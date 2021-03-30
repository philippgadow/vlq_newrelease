'''
Script to hack lhe files with complete decay chain to refurbish it into
an lhe file with partial decay chain iformation. Should be usable for single
VLQ (X, T, B, Y) production with decays restricted to 3rd gen SM quarks.

Developed by: Avik Roy
Institute: UT Austin
'''

import sys, math, os, subprocess

def collapse(_list, mode):
    px = float(_list[6])
    py = float(_list[7])
    pz = float(_list[8])
    e_0 = float(_list[9])
    if mode == 23:   # Z
        mass = 9.1187600000e+01
    elif mode == 6:  # t
        mass = 172.0
    elif mode == 5:  # b
        mass = 4.70000e+00
    elif mode == 24:  # W
        mass = 7.9824360e+01
    elif mode == 25:  # H
        mass = 1.250000e+02
    else:
        mass = float(_list[10])
    e = math.sqrt(px**2 + py**2 + pz**2 + mass**2)
    dE = e - e_0
    return [e, mass, dE]
    
def adjust(_list, dE):
    px = float(_list[6])
    py = float(_list[7])
    pz = float(_list[8])
    e_0 = float(_list[9])
    m_0 = float(_list[10])
    
    e = e_0 + dE
    m2 = e**2 - (px**2 + py**2 + pz**2)
    if m2 < 0:
        print("invariant mass is going to be imaginary")
    mass = math.sqrt(m2)
    _list[9] = str(e)
    _list[10] = str(mass)
    return "  ".join(_list) + "\n"
    
def tweak_parton(_list, dE):
    e_0 = float(_list[9])
    pz_0 = float(_list[8])
    e = e_0 + dE
    pz = (pz_0/abs(pz_0))*e
    _list[8] = str(pz)
    _list[9] = str(e)

    return "  ".join(_list) + "\n"

    
def particlemapper(_list):
    particles = {}
    for ii in range(1,len(_list)):
        this_line = _list[ii].strip().split()
        particlemap = {}
        particlemap['id'] = int(this_line[0])
        particlemap['status'] = int(this_line[1])
        particlemap['parent0'] = int(this_line[2])
        particlemap['parent1'] = int(this_line[3])
        particlemap['px'] = float(this_line[6])
        particlemap['py'] = float(this_line[7])
        particlemap['pz'] = float(this_line[8])
        particlemap['e'] = float(this_line[9])
        particlemap['m'] = float(this_line[10])
        particlemap['keepit'] = True
        particlemap['spin'] = float(this_line[12])
        particles[ii] = particlemap
    return particles

def fix_list(particlelist, VLQMode, fermchild, bosonchild):
    #for ii in particlelist: print ii
    new_list = []
    new_list.append(particlelist[0])
    particles = particlemapper(particlelist)

    def propagate(key, dE):
        particles[key]['e'] = particles[key]['e'] + dE
        if particles[key]['parent0'] != 0 and particles[key]['parent1'] !=0: ## not a parton
            particles[key]['m'] = math.sqrt(particles[key]['e']**2 - particles[key]['px']**2 - particles[key]['py']**2 - particles[key]['pz']**2)
            propagate(particles[key]['parent0'], dE/2.)
            propagate(particles[key]['parent1'], dE/2.)
        else:
            particles[key]['pz'] = (particles[key]['pz']/abs(particles[key]['pz']))*particles[key]['e']


    def not_in_decay_chain(particle):
        if particle['parent0'] == 0:
            return True
        if particles[particle['parent0']]['parent0'] == 0:
            return True
        if abs(particles[particle['parent0']]['id']) in [bosonchild, fermchild] and abs(particles[particles[particle['parent0']]['parent0']]['id']) == VLQMode:  # children of boson/fermion from VLQ decay
            return False
        if abs(particles[particle['parent0']]['id']) == 6: #children of top decay
            return False
        else:
            return not_in_decay_chain(particles[particle['parent0']])

        
    for key in sorted(particles.keys()):
        this_particle = particles[key]
        if this_particle['parent0'] == 0 and this_particle['parent1'] == 0: continue
        this_list = particlelist[key].strip().split()
        if abs(this_particle['id']) == bosonchild and (abs(particles[this_particle['parent0']]['id']) == VLQMode or abs(particles[this_particle['parent1']]['id']) == VLQMode) and this_particle['status'] == 2: ## Decayed Bosonic child (W, Z, H)
            [ this_particle['e'], this_particle['m'], dE ] = collapse(this_list, bosonchild)
            propagate(this_particle['parent0'], dE/2.)
            propagate(this_particle['parent1'], dE/2.)
            this_particle['status'] = 1
        #elif abs(this_particle['id']) == fermchild and (abs(particles[this_particle['parent0']]['id']) == VLQMode and abs(particles[this_particle['parent1']]['id'] == VLQMode) and this_particle['status'] == 2: ## Decayed Fermionic child (t, b)
        elif abs(this_particle['id']) == 6 and this_particle['status'] == 2: ## Intermediate top quark
            [ this_particle['e'], this_particle['m'], dE ] = collapse(this_list, 6)
            propagate(this_particle['parent0'], dE/2.)
            propagate(this_particle['parent1'], dE/2.)
            this_particle['status'] = 1
            #if fermchild == 6:   # Fix the helicity/spin, only needed if the fermionic child is a top
            for _key in sorted(particles.keys()):
                _this_particle = particles[_key]
                if abs(_this_particle['id']) == 5 and abs(particles[_this_particle['parent0']]['id']) == 6 and particles[particles[_this_particle['parent0']]['parent0']]['id'] == particles[this_particle['parent0']]['id']: ## b from the current t
                    this_particle['spin'] = _this_particle['spin']
        else:
            this_particle['keepit'] = not_in_decay_chain(this_particle)
        # elif abs(particles[this_particle['parent0']]['id']) in [bosonchild, fermchild]:   
        #     ## Grandchildren of T, to be ommitted from lhe
        #     #print "Ommitting: \n\n"
        #     #print this_particle
        #     this_particle['keepit'] = False
        # elif particles[this_particle['parent0']]['parent0'] != 0:
        #     if abs(particles[particles[this_particle['parent0']]['parent0']]['id']) == 6: 
        #         ## grand-grand children of T, to be
        #         #print "Ommitting: \n\n"
        #         #print this_particle
        #         this_particle['keepit'] = False
        
    to_keep = 0
    for key in particles:
        if particles[key]['keepit']: to_keep += 1

    first_line_info = new_list[0].split()
    first_line_info[0] = str(to_keep)
    #print_tag = False
    #if int(first_line_info[0]) != 7: print_tag = True
    this_line_now = "  ".join(first_line_info) + '\n'
    new_list[0] = this_line_now
    
    for key in sorted(particles.keys()):
        if particles[key]['keepit'] == False:
            #print key
            for _key in sorted(particles.keys()):
                #if _key <= key: continue
                #print "changing key = ", _key
                if particles[_key]['parent0'] > key: 
                    #print "changing parent of ", _key, " from ", particles[_key]['parent0'], " to ", particles[_key]['parent0'] - 1
                    particles[_key]['parent0'] = particles[_key]['parent0'] - 1
                    #print particles[_key]['parent0']
                if particles[_key]['parent1'] > key: particles[_key]['parent1'] = particles[_key]['parent1'] - 1
    
    for key in sorted(particles.keys()):
        this_particle = particles[key]
        if not this_particle['keepit']: continue
        this_list = particlelist[key].strip().split()
        this_list[1] = str(this_particle['status'])
        this_list[2] = str(this_particle['parent0'])
        this_list[3] = str(this_particle['parent1'])
        this_list[6] = str(this_particle['px'])
        this_list[7] = str(this_particle['py'])
        this_list[8] = str(this_particle['pz'])
        this_list[9] = str(this_particle['e'])
        this_list[10] = str(this_particle['m'])
        this_list[12] = str(this_particle['spin'])
        new_list.append("  ".join(this_list) + "\n")
        
    #for ii in range(len(new_list)): print new_list[ii]
    #sys.exit(1)
    return new_list

def lhe_hacker(lhe_minDecay='./events_MinimalDecay.lhe', lhe_fullDecay='./events_FullDecay.lhe', vlq='T', decay='Z'):

    if vlq == 'X' or vlq == 'x' or vlq == 6000005:  # Only allowed decay, X > W t
        VLQMode = 6000005
        fermchild = 6
        bosonchild = 24
    elif vlq == 'B' or vlq == 'bp' or vlq == 6000007: 
        VLQMode = 6000007
        if decay == 'W' or decay == 24:  # B > W t
            fermchild = 6
            bosonchild = 24
        elif decay == 'H' or decay == 23: # B > H b
            fermchild = 5
            bosonchild = 25
        else:                             # B > Z b
            fermchild = 5
            bosonchild = 23
    elif vlq == 'Y' or vlq == 'y' or vlq == 6000008: # Only allowed decay, Y > W b
        VLQMode = 6000008
        fermchild = 5
        bosonchild = 24
    else:   # Choose the default, T
        VLQMode = 6000006
        if decay == 'W' or decay == 24:  # T > W b
            fermchild = 5
            bosonchild = 24
        elif decay == 'H' or decay == 23: # T > H t
            fermchild = 6
            bosonchild = 25
        else:                             # T > Z t
            fermchild = 6
            bosonchild = 23
            
    fulldecay = lhe_fullDecay
    mindecay  = lhe_minDecay

    if not os.path.exists(mindecay):
        if '.gz' not in mindecay: mindecay += '.gz'
        elif '.gz' in mindecay: mindecay = mindecay.replace('.gz','')
        if not os.path.exists(mindecay):
            print("ERROR! lhe file with minimal decay not found. Refurbishing cannot be done")
            return False
    
    if not os.path.exists(fulldecay):
        if '.gz' not in fulldecay: fulldecay += '.gz'
        elif '.gz' in fulldecay: fulldecay = fulldecay.replace('.gz','')
        if not os.path.exists(fulldecay):
            print("ERROR! lhe file with full decay not found. Refurbishing cannot be done")
            return False

    if '.gz' in fulldecay:
        subprocess.call('gunzip  ' + fulldecay, shell=True)
        fulldecay = fulldecay.replace('.gz','')
    if '.gz' in mindecay:
        subprocess.call('gunzip ' + mindecay, shell=True)
        mindecay = mindecay.replace('.gz','')
    

    file_full = open(fulldecay, "r")
    file_min  = open(mindecay, "r")
    file_final = open("unweighted_events.lhe","w")

    for line in file_min:
        if "<MGRunCard>" in line:
            break
        file_final.write(line)


    skip_tag = True
    line = file_full.next()

    while "<event>" not in line:
        if "<MGRunCard>" in line and skip_tag: skip_tag = False
        if not skip_tag: file_final.write(line)
        line = file_full.next()

    #print line.strip()

    while True:
        try:
            event_lines = []
            mgrwt_lines = []
            in_mgrwt_block = False
            while line:
                if "</event>" in line:
                    break
                #elif "</rwgt>" in line:
                #    mgrwt_lines.append(line)
                #    in_mgrwt_block = False
                #    line = file_full.next()
                elif "<event>" in line:
                    in_mgrwt_block = False
                    file_final.write(line)
                    line = file_full.next()
                elif "<mgrwt>" in  line or in_mgrwt_block:
                    in_mgrwt_block = True
                    mgrwt_lines.append(line)
                    line = file_full.next()
                else:
                    #print line
                    event_lines.append(line)
                    line = file_full.next()
            #print " \n\n\n Initial set \n\n"
            #for line in event_lines: print line

            event_lines = fix_list(event_lines, VLQMode, fermchild, bosonchild)


            #print " \n\n\n Final set \n\n"
            #for line in event_lines: print line
            first_line_info = event_lines[0].split()
            #first_line_info[0] = str(int(first_line_info[0]) - 6)
            #print_tag = False
            #if int(first_line_info[0]) != 7: print_tag = True
            this_line_now = "  ".join(first_line_info) + '\n'
            file_final.write(this_line_now)
            for ii in range(1, len(event_lines)):
                #if print_tag: print event_lines[ii].strip()
                line_info = event_lines[ii].strip().split()
                this_line_now = "  ".join(line_info) + '\n'
                file_final.write(this_line_now)
                # if abs(float(line_info[0])) == float(bosonchild):
                #     Z_index = ii
                #     line_info[1] = "1"
                #     this_line_now = "  ".join(line_info) + '\n'
                #     file_final.write(this_line_now)
                # elif abs(float(line_info[0])) == float(fermchild):
                #     t_index = ii
                #     line_info[1] = "1"
                #     this_line_now = "  ".join(line_info) + '\n'
                #     file_final.write(this_line_now)
                # else:
                #     this_line_now = "  ".join(line_info) + '\n'
                #     file_final.write(this_line_now)
            for rwtline in mgrwt_lines:
                file_final.write(rwtline)
            file_final.write("</event>\n")
            line = file_full.next()
        except StopIteration:
            break

    file_final.write("</LesHouchesEvents>\n")
    file_full.close()
    file_min.close()
    file_final.close()
    return True

def weightblock_maker(wts, tagmap):
    str_to_write = '<rwgt>\n'
    for key in sorted(tagmap.keys()):
        if tagmap[key] == 'nominal': 
            continue
        else:
            wtname = str(tagmap[key])
            wtval = str(wts[wtname])
            str_to_write += '''<wgt id='%s'> %s </wgt>\n'''%(wtname, wtval)
    str_to_write += '</rwgt>\n'
    return str_to_write

def placeback(lhe_fullDecay,lhe_reweighted):

    fulldecay = lhe_fullDecay
    reweighted = lhe_reweighted 

    if not os.path.exists(fulldecay):
        if '.gz' not in fulldecay: fulldecay += '.gz'
        elif '.gz' in fulldecay: fulldecay = fulldecay.replace('.gz','')
        if not os.path.exists(fulldecay):
            print("ERROR! lhe file with full decay not found. Placeback cannot be done")
            return False
    
    if not os.path.exists(reweighted):
        print("ERROR! lhe file with reweighting not found. Placeback cannot be done")
        return False

    if '.gz' in reweighted:
        print "unpacking " + reweighted
        subprocess.call('gunzip ' + reweighted, shell=True)
        reweighted = reweighted.replace('.gz','')
    if '.gz' in fulldecay:
        subprocess.call('gunzip ' + fulldecay, shell=True)
        fulldecay = fulldecay.replace('.gz','')

    #reweighted_event_dict = lhe_to_dict(reweighted)
    

    newlhe = open('tmp_final_events.events','w')
    oldlhe = open(fulldecay,'r')
    rewtlhe = open(reweighted,'r')

    is_rwt_ok = False
    for line in rewtlhe:
        if '<initrwgt>' in line:
            is_rwt_ok = True
            break

    if not is_rwt_ok:
        print("ERROR! Reweighted lhe exists but does not contain reweighting information. Reweighting probably failed")
        return False

    rewtlhe.close()
    rewtlhe = open(reweighted,'r')

    ## First create the <initrwgt> block from reweighted lhe

    initrwgt_block = ''
    found_block = False
    weight_tags = {}
    weight_tag_count = 0
    while True:
        try:
            line = rewtlhe.next()
            if '<initrwgt>' not in line and not found_block:
                continue
            else:
                #print line
                found_block = True
                initrwgt_block += line.strip() + '\n'
                if "weight id" in line:
                    _tag = line.replace("'",'').split('=')[1].split('>')[0].strip()
                    weight_tags[weight_tag_count] = _tag
                    weight_tag_count += 1
                if '</initrwgt>' in line:
                    break
        except StopIteration:
            break

    evcount = 0
    
    weight_info = {}
    this_wts = ''
    while True:
        try:
            line = rewtlhe.next()
            if '<rwgt>' in line or '</rwgt>' in line or '<wgt id=' in line:
                this_wts += line.strip() + '\n'
            elif '</event>' in line:
                weight_info[evcount] = this_wts
                evcount += 1
                this_wts = ''
            else:
                continue
        except StopIteration:
            break

    evcount = 0

    while True:
        try:
            line = oldlhe.next()
            if '<MGGenerationInfo>' in line:
                newlhe.write(initrwgt_block)
                newlhe.write(line)
            elif '</event>' in line:
                #these_wts = weightblock_maker(reweighted_event_dict[evcount]['wts'],weight_tags)
                newlhe.write(weight_info[evcount])
                newlhe.write(line)
                evcount += 1
            elif '<rwgt>' in line or '</rwgt>' in line or '<wgt id=' in line:
                #line = oldlhe.next()
                continue
            else:
                newlhe.write(line)
        except StopIteration:
            break
    
    newlhe.flush()
    newlhe.close()
    oldlhe.close()
    rewtlhe.close()
    return True

