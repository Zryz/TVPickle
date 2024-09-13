
def tvpickle_controls(tvpickle)->dict:
    return {
        'intro':{' ': [ [tvpickle.ui.select_page, {'name':'mode'}], [tvpickle.ui.controls.select, {'control_name':'mode'}]]},
        'discover':{'g':[[tvpickle.ui.controls.select,{'control_name':'genre_menu'}]],
                    'enter':[[tvpickle.build_result_page]]},
        'mode':{    's':[[tvpickle.init_discover_mode, {'app_mode':'Search'}]], 
                    'S':[[tvpickle.init_discover_mode, {'app_mode':'Search'}]], 
                    'm':[[tvpickle.init_discover_mode, {'app_mode':'Movie'}]], 
                    'M':[[tvpickle.init_discover_mode, {'app_mode':'Movie'}]], 
                    't':[[tvpickle.init_discover_mode, {'app_mode':'TV'}]],
                    'T':[[tvpickle.init_discover_mode, {'app_mode':'TV'}]] },
        'results':{ 'left':[[tvpickle.prev_result]], 
                    'right':[[tvpickle.next_result]]}      
        }

