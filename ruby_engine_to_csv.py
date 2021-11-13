#######################################################################################################
#######################################################################################################
#######################################################################################################

## input: service product mapping ruby code
## output: visual representation of product map

#######################################################################################################
#######################################################################################################
#######################################################################################################

### packages ###
import csv 
import re 

### variables ###

## lists
csv_columns = ['AWS Category', 'Categories']

## files
new_prod_map = 'prod_map.csv'
prod_map_lines=open('AwsService.rb', 'r').read().splitlines()

### functions ###
def prodenator(da_map):
    ### creates dictionary that contain the product and the function used to map it
    prod_maps = {}

    for line in da_map:
        prod_map_dict = {}
        sline = line.strip()

        if re.search('^\'.*?map_with.*?name.*?},$', sline):
            product = re.findall('\'(.*?)\'', sline)
            map_with = re.findall('map_with: :(.*?),', sline)
            prod_map_dict[product[0]] = map_with[0]
            prod_maps.update(prod_map_dict)

    return prod_maps

def static_stuff_handler(dumb_stuff):
    dumb_dict = {
        'ut.blank?': {'ut': 'IS_BLANK'},'ut.present?': {'ut': 'IS_NOT_BLANK'},"ut.downcase.include? 'detect'": {'ut':'/detect/'},"ut.downcase.include? 'usage'": {'ut' : '/usage/'},"ut.downcase.include? 'storage'": {'ut':'/storage/'},'ut.nil?': {'ut':'IS_BLANK'},
        'no_resource': {'resource_id': 'IS_BLANK'},'resource_id.present?': {'resource_id': 'IS_NOT_BLANK'},'!resource_id.nil?': {'resource_id': 'IS_NOT_BLANK'},'present_and_not_null?(resource_id)': {'resource_id': 'IS_NOT_BLANK'},'resource_id.nil?': {'resource_id': 'IS_BLANK'},'resource_id.blank?':{'resource_id': 'IS_BLANK'},
        "descr.include? '(Standard Edition)'": {'descr':'/Standard Edition/'}, 'descr': {'descr': 'IS_NOT_BLANK'},"descr.include?('hours used')": {'descr': '/hours used/'},"descr.include? 'Sign up charge for subscription'": {'descr': '/Sign up charge for subscription/'},"descr.include?('hours used') # unused RI's.": { 'descr': '/hours used/'},
        'other_return_d.nil?' : {'cost': 'OTHER'},'other_return_i': {'cost': 'OTHER'},
        'invoice_map': {'cost': 'OTHER'},
        "(oper.include? 'Storage')": {'oper':'/Storage/'},"oper.include? 'Storage'": {'oper':'/Storage/'},"oper.include? 'Request'": {'oper':'/Request/'},"oper.include? 'Job'": {'oper':'/Job/'},"oper.include? 'DevEndpoint'": {'oper':'/DevEndpoint/'},"oper.include? 'Crawler'": {'oper':'/Crawler/'},"oper.include?('Instance')": {'oper':'/Instance/'},"oper.include?('Spot')": {'oper':'/Spot/'},'oper.blank?':{'oper':'IS_BLANK'}
    }

    return dumb_dict[dumb_stuff]

def if_handler(piece, if_dict, if_type):
    if if_type not in if_dict:
        if_dict[if_type] = {}

    if re.search('[<>=]', piece):
        logic_split = re.split('[<>]|=.',piece) 

        if logic_split[0].strip() in if_dict[if_type]:
            if_dict[if_type][logic_split[0].strip()].append(logic_split[1].strip())
        else:
            if_dict[if_type][logic_split[0].strip()] = []
            if_dict[if_type][logic_split[0].strip()].append(logic_split[1].strip())

    else:
        other_piece = static_stuff_handler(piece.strip())
        other_piece_key = list(other_piece.keys())[0]

        if other_piece_key in if_dict[if_type]:
            if_dict[if_type][other_piece_key].append(other_piece[other_piece_key])
        else:
            if_dict[if_type][other_piece_key] = []
            if_dict[if_type][other_piece_key].append(other_piece[other_piece_key])
    
    return if_dict

def return_if_handler(piece, obj_dict, func_name, map_obj, if_type):
    if if_type not in obj_dict[func_name][map_obj]:
        obj_dict[func_name][map_obj][if_type] = {}

    if re.search('[<>=]', piece):
        logic_split = re.split('[<>]|=.',piece)

        if logic_split[0].strip() in obj_dict[func_name][map_obj][if_type]:
            obj_dict[func_name][map_obj][if_type][logic_split[0].strip()].append(logic_split[1].strip())
        else:
            obj_dict[func_name][map_obj][if_type][logic_split[0].strip()] = []
            obj_dict[func_name][map_obj][if_type][logic_split[0].strip()].append(logic_split[1].strip())

    else:
        other_piece = static_stuff_handler(piece.strip())
        other_piece_key = list(other_piece.keys())[0]

        if other_piece_key in obj_dict[func_name][map_obj][if_type]:
            obj_dict[func_name][map_obj][if_type][other_piece_key].append(other_piece[other_piece_key])
        else:
            obj_dict[func_name][map_obj][if_type][other_piece_key] = []
            obj_dict[func_name][map_obj][if_type][other_piece_key].append(other_piece[other_piece_key])
    
    return obj_dict

def map_funcenator(da_map, static_stuff_handler, prod_map, if_handler, return_if_handler):
    ### creates dictionary that contains name of the function and all lines within each function 
    all_funcs = {}
    func_dict = {}
    obj_dict = {}
    if_dict = {}

    ends_needed = 0
    ends_captured = 0
    if_ends_needed = 0
    case_ends_needed = 0
    when_needed = 0

    for line in da_map:
        sline = line.strip()

        if re.search(r'^def.*?_map.*', sline):
            func_name = re.findall(r'\.(.*?)\(', sline)
            ends_needed += 1 
            
        # return iffer
        if ends_needed >= 1 and not re.search('^def.*?_map.*', sline):

            ###################################################################################
            ## solve plain return 
            ###################################################################################

            if re.search(r'^return\s*[A-Z\d_]{2,}$',sline) and func_name[0] in prod_map.values():
                map_obj = re.findall(r'^return\s([A-Z_\d]{2,})',sline)
                if func_name[0] not in obj_dict:
                    obj_dict[func_name[0]] = {}
                if map_obj[0] not in obj_dict[func_name[0]]:
                    obj_dict[func_name[0]][map_obj[0]] = {}

                # print(func_name[0]+' :: '+map_obj[0])

            ###################################################################################
            ## solve ifs 
            ###################################################################################

            if (sline[:2] == 'if' or sline[:5] == 'elsif') and func_name and func_name[0] in prod_map.values():
                if sline[:2] == 'if':
                    if_ends_needed += 1
                    ends_needed += 1
                # grab logic from if statement
                print(sline)
                logics = re.findall(r'\w*?if\s*(.*)', sline)
                print(logics)
                logic = logics[0]

                ###################################################################################
                ## solve ifs with parentheses 
                ###################################################################################
                if re.search(r'[&|]{2}\s*\((.*?)\)',logic):
                    parens = re.findall(r'[&|]{2}\s*\((.*?)\)', logic)
                    nonparens = re.findall(r'\w*?if(.*?)[&|]{2}\s*\(.*?\)', sline)

                    ## solve parens with and inside
                    if re.search(r'&&',parens[0]):
                        paren_type = 'AND_PARENS'
                        logic_pieces = re.split(r'&&', parens[0])
                        
                        for piece in logic_pieces:
                            if_dict = if_handler(piece, if_dict, paren_type)
                        
                    ## solve parens with or inside
                    elif re.search(r'\|\|',parens[0]):
                        paren_type = 'OR_PARENS'
                        logic_pieces = re.split(r'\|\|', parens[0])
                        
                        for piece in logic_pieces:
                            if_dict = if_handler(piece, if_dict, paren_type)
                        
                    ## solve parens with no and or inside
                    else:
                        paren_type = 'PARENS'
                        if_dict = if_handler(parens[0], if_dict, paren_type)
                    
                    ## add in everything outside of parens
                    paren_type = 'OUTSIDE_PARENS'
                    if_dict = if_handler(nonparens[0], if_dict, paren_type)
                        
                    ## how to deal with parens when adding it all together
                    if re.search(r'&{2}\s\(.*?\)',sline):
                        if_dict['PAREN_DEAL'] = 'AND'
                    else:
                        if_dict['PAREN_DEAL'] = 'OR'

                ###################################################################################
                ## solve for ifs with no parentheses
                ###################################################################################
                else:
                    ## solve ands
                    if re.search(r'&&',logic):
                        if_type = 'AND_LOGIC'
                        logic_pieces = re.split(r'&&', logic)
                        
                        for piece in logic_pieces:
                            if_dict = if_handler(piece, if_dict, if_type)

                    ## solve ors
                    elif re.search(r'\|\|',logic):
                        if_type = 'OR_LOGIC'
                        logic_pieces = re.split(r'\|\|', logic)
                        
                        for piece in logic_pieces:
                            if_dict = if_handler(piece, if_dict, if_type)

                    ## solve no and or 
                    else:
                        if_type = 'LOGIC'
                        if_dict = if_handler(logic, if_dict, if_type)

            ###################################################################################
            ## solve return ifs 
            ###################################################################################
            if re.search(r'^return\s[A-Z_\d]{2,}\s*if',sline):
                ## name of object used to map to label
                map_obj = re.findall(r'^return\s([A-Z_\d]{2,})',sline)

                # create function and object in object dict if does not exist
                if func_name[0] not in obj_dict:
                    obj_dict[func_name[0]] = {}

                if map_obj[0] not in obj_dict[func_name[0]]:
                    obj_dict[func_name[0]][map_obj[0]] = {}

                # grab logic from if statement
                logics = re.findall(r'.*?if\s(.*)#*.*', sline)
                logic = logics[0]

                ###################################################################################
                ## solve parentheses 
                ###################################################################################
                if re.search(r'[&|]{2}\s\((.*?)\)',logic):
                    parens = re.findall(r'[&|]{2}\s\((.*?)\)', sline)
                    nonparens = re.findall(r'if(.*?)[&|]{2}\s\(.*?\)', sline)

                    ## solve parens with and inside
                    if re.search(r'&&',parens[0]):
                        if_type = 'AND_PARENS'
                        logic_pieces = re.split(r'&&', parens[0])
                        
                        for piece in logic_pieces:
                            if map_obj[0] in obj_dict[func_name[0]]:
                                obj_dict.update(return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type))
                            else:
                                obj_dict = return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type)

                    ## solve parens with or inside
                    elif re.search(r'\|\|',parens[0]):
                        if_type = 'OR_PARENS'
                        logic_pieces = re.split(r'\|\|', parens[0])
                        
                        for piece in logic_pieces:
                            if map_obj[0] in obj_dict[func_name[0]]:
                                obj_dict.update(return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type))
                            else:
                                obj_dict = return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type)

                    ## solve parens with no and or inside
                    else:
                        if_type = 'PARENS'
                        if map_obj[0] in obj_dict[func_name[0]]:
                            obj_dict.update(return_if_handler(parens[0], obj_dict, func_name[0], map_obj[0], if_type))
                        else:
                            obj_dict = return_if_handler(parens[0], obj_dict, func_name[0], map_obj[0], if_type)

                    ## add in everything outside of parens
                    if_type = 'OUTSIDE_PARENS'
                    if map_obj[0] in obj_dict[func_name[0]]:
                        obj_dict.update(return_if_handler(nonparens[0], obj_dict, func_name[0], map_obj[0], if_type))
                    else:
                        obj_dict = return_if_handler(nonparens[0], obj_dict, func_name[0], map_obj[0], if_type)

                    ## how to deal with parens when adding it all together
                    if re.search(r'&{2}\s\(.*?\)',logics[0] ):
                        obj_dict[func_name[0]][map_obj[0]]['PAREN_DEAL'] = 'AND'
                    else:
                        obj_dict[func_name[0]][map_obj[0]]['PAREN_DEAL'] = 'OR'

                ###################################################################################
                ## solve for return ifs with no parentheses
                ###################################################################################
                else:
                    
                    ## solve ands
                    if re.search(r'&&',logic):
                        if_type = 'AND_LOGIC'
                        logic_pieces = re.split(r'&&', logic)
                        
                        for piece in logic_pieces:
                            if map_obj[0] in obj_dict[func_name[0]]:
                                obj_dict.update(return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type))
                            else:
                                obj_dict = return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type)

                    ## solve ors
                    elif re.search(r'\|\|',logic):
                        if_type = 'OR_LOGIC'
                        logic_pieces = re.split(r'\|\|', logic)
                        
                        for piece in logic_pieces:
                            if map_obj[0] in obj_dict[func_name[0]]:
                                obj_dict.update(return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type))
                            else:
                                obj_dict = return_if_handler(piece, obj_dict, func_name[0], map_obj[0], if_type)

                    ## solve no and or 
                    else:
                        if_type = 'LOGIC'
                        if map_obj[0] in obj_dict[func_name[0]]:
                            obj_dict.update(return_if_handler(logic, obj_dict, func_name[0], map_obj[0], if_type))
                        else:
                            obj_dict = return_if_handler(logic, obj_dict, func_name[0], map_obj[0], if_type)

            ###################################################################################
            ## solve cases 
            ###################################################################################

            if sline[:4] == 'case'and func_name and func_name[0] in prod_map.values():
                # if 'CASE_DICT' not in obj_dict[func_name[0]][map_obj[0]]
                case_ends_needed += 1
                ends_needed += 1
                when_needed += 1
                
            ###################################################################################
            ## closing ifs
            ###################################################################################

            if if_ends_needed >= ends_captured and func_name[0] in prod_map.values():
                if func_name[0] in obj_dict:
                    if map_obj[0] in obj_dict[func_name[0]]:
                        if 'IF_DICT' in obj_dict[func_name[0]][map_obj[0]]:
                            obj_dict[func_name[0]][map_obj[0]]['IF_DICT'].update(if_dict)
                        else:
                            obj_dict[func_name[0]][map_obj[0]]['IF_DICT'] = if_dict

            if ends_needed > 0 and sline == 'end':
                ends_captured += 1

                # print('needed :: ' + str(ends_needed))
                # print('captured :: ' + str(ends_captured))

            if if_ends_needed == ends_captured:
                # print('needed :: ' + str(ends_needed))
                # print('captured :: ' + str(ends_captured))
                if_ends_needed = 0
                if_dict = {}

            if ends_needed == ends_captured:
                # print(func_name[0])
                all_funcs.update(func_dict)
                func_dict = {}
                func_dict['func_lines'] = []
                ends_captured = 0
                ends_needed = 0

    print(obj_dict)

    # return all_funcs

def map_grabenator(da_map):
    ### creates dictionary that contains the map name and all lines within each map 
    all_maps = {}
    maps_dict = {}
    closes_needed = 0
    closes_captured = 0

    for amap in da_map:
        sline = amap.strip()

        if re.search(r'^[A-Z_\d]+_(MAP|OPERATION)\s=\s{$',sline):
            map_name = re.findall(r'^[A-Z_\d]+', sline)
            closes_needed += 1
        elif re.search(r'=>', sline):
            maps_line = re.findall(r'([A-Z_\d]+),$', sline)
            if len(maps_line) > 0:
                if map_name[0] in maps_dict:
                    maps_dict[map_name[0]].append(maps_line[0])
                else:
                    maps_dict[map_name[0]] = []
                    maps_dict[map_name[0]].append(maps_line[0])
        elif sline == '}':
            closes_captured += 1

        if closes_needed == closes_captured:
            all_maps.update(maps_dict)
            maps_dict = {}
            closes_needed = 0
            closes_captured = 0

    return all_maps

def label_grabenator(da_map):
    ### creates dictionary of map_objects to CH labels

    all_labels = {}

    for line in da_map:
        label_dict = {}
        sline = line.strip()

        if re.search(r'^add ([A-Z_\d]+)',sline):
            map_obj = re.findall(r'add ([A-Z_\d]+)',sline)
            obj_label = re.findall(r'label:\s*\'(.*?)\'',sline)
            label_dict[map_obj[0]] = obj_label[0]

            all_labels.update(label_dict)

    return all_labels

def stickitogetherenator(prods, funcs, maps, labels):
    ### creates final map, piecing all objects together
    pre_map = {}
    mid_map = {}
    final_map = {}

    for prod in prods:
        
        if prods[prod] in funcs:
            for func in funcs[prods[prod]]:
                map_obj = re.findall(r'[A-Z_\d]{2,}', func)

                if map_obj and map_obj[0] in labels:
                    if prods[prod] in pre_map:
                        pre_map[prods[prod]].append(map_obj[0])
                    else:
                        pre_map[prods[prod]] = []
                        pre_map[prods[prod]].append(map_obj[0])

                map_map = re.findall(r'[A-Z_\d]+_MAP', func)
                
                if map_map and map_map[0] in maps:
                    if prods[prod] in pre_map:
                        pre_map[prods[prod]] = maps[map_map[0]] + pre_map[prods[prod]]
                    else:
                        pre_map[prods[prod]] = []
                        pre_map[prods[prod]] = maps[map_map[0]] + pre_map[prods[prod]]

        if prods[prod] in pre_map:
            mid_map[prod] = pre_map[prods[prod]]

    for service in mid_map:
        for map_obj in mid_map[service]:
            if map_obj in labels:

                if service in final_map:
                    final_map[service].append(labels[map_obj])
                else:
                    final_map[service] = []
                    final_map[service].append(labels[map_obj])

    return final_map

### script ###
if __name__ == "__main__":

    ### process that jazz

    prods = prodenator(prod_map_lines)

    # funcs = map_funcenator(prod_map_lines)
    map_funcenator(prod_map_lines, static_stuff_handler, prods, if_handler, return_if_handler)
    # funcexplodenator(funcs)

    maps = map_grabenator(prod_map_lines)

    labels = label_grabenator(prod_map_lines)

    # final_map_dict = stickitogetherenator(prods, funcs, maps, labels)

    ## write the csv
    # with open('simple_map.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for key, value in final_map_dict.items():
    #         for obj in value:
    #             writer.writerow([key, obj])
