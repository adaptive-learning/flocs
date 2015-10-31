/*
 * Blocks constant
 */
angular.module('flocs.workspace')
.constant('blocks', {
    'maze_category':'<category name="Maze">' +
        '<block type="maze_move_forward"></block>' +
        '<block type="maze_move_backward"></block>' +
        '<block type="maze_turn"></block>' +
        '<block type="maze_check_path"></block>' +
        '<block type="maze_check_bomb"></block>' +
        '<block type="maze_check_color"></block>' +
        '</category>',

    'variables_category':'<category name="Variables" custom="VARIABLE"></category>',
    'functions_category':'<category name="Functions" custom="PROCEDURE"></category>',

    'if_category':'<category name="If">' +
        '<block type="controls_if"></block>' +
        '<block type="controls_if">' +
        '<mutation else="1"></mutation>' +
        '</block>' +
        '<block type="controls_if">' +
        '<mutation elseif="1" else="1"></mutation>' +
        '</block>' +
        '</category>', 

    'controls_if_else':'<block type="controls_if">' +
        '<mutation else="1"></mutation>' +
        '</block>', 

    'constrols_if_elseif_else':'<block type="controls_if">' +
        '<mutation elseif="1" else="1"></mutation>' +
        '</block>', 

    'loops_category':'<category name="Loops">' +
        '<block type="controls_repeat_ext">' +
        '<value name="TIMES">' +
        '<block type="math_number">' +
        '<field name="NUM">10</field>' +
        '</block>' +
        '</value>' +
        '</block>' +
        '<block type="controls_while"></block>' +
        '<block type="controls_for">' +
        '<field name="VAR">i</field>' +
        '<value name="FROM">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '<value name="TO">' +
        '<block type="math_number">' +
        '<field name="NUM">10</field>' +
        '</block>' +
        '</value>' +
        '<value name="BY">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '</block>' +
        '<block type="controls_forEach"></block>' +
        '<block type="controls_flow_statements"></block>' +
        '</category>', 

    'controls_repeat':'<block type="controls_repeat_ext">' +
        '<value name="TIMES">' +
        '<block type="math_number">' +
        '<field name="NUM">10</field>' +
        '</block>' +
        '</value>' +
        '</block>', 

    'constrols_for':'<block type="controls_for">' +
        '<field name="VAR">i</field>' +
        '<value name="FROM">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '<value name="TO">' +
        '<block type="math_number">' +
        '<field name="NUM">10</field>' +
        '</block>' +
        '</value>' +
        '<value name="BY">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '</block>', 

    'boolean_category':'<category name="Boolean">' +
        '<block type="logic_compare"></block>' +
        '<block type="logic_operation"></block>' +
        '<block type="logic_negate"></block>' +
        '<block type="logic_boolean"></block>' +
        '<block type="logic_null"></block>' +
        '<block type="logic_ternary"></block>' +
        '</category>' ,

    'math_category':'<category name="Math">' +
        '<block type="math_number"></block>' +
        '<block type="math_arithmetic"></block>' +
        '<block type="math_single"></block>' +
        '<block type="math_trig"></block>' +
        '<block type="math_constant"></block>' +
        '<block type="math_number_property"></block>' +
        '<block type="math_change">' +
        '<value name="DELTA">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '</block>' +
        '<block type="math_round"></block>' +
        '<block type="math_on_list"></block>' +
        '<block type="math_modulo"></block>' +
        '<block type="math_constrain">' +
        '<value name="LOW">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '<value name="HIGH">' +
        '<block type="math_number">' +
        '<field name="NUM">100</field>' +
        '</block>' +
        '</value>' +
        '</block>' +
        '<block type="math_random_int">' +
        '<value name="FROM">' +
        '<block type="math_number">' +
        '<field name="NUM">1</field>' +
        '</block>' +
        '</value>' +
        '<value name="TO">' +
        '<block type="math_number">' +
        '<field name="NUM">100</field>' +
        '</block>' +
        '</value>' +
        '</block>' +
        '<block type="math_random_float"></block>' +
        '</category>',

    'lists_category':'<category name="Lists">' +
        '<block type="lists_create_empty"></block>' +
        '<block type="lists_create_with"></block>' +
        '<block type="lists_repeat">' +
        '<value name="NUM">' +
        '<block type="math_number">' +
        '<field name="NUM">5</field>' +
        '</block>' +
        '</value>' +
        '</block>' +
        '<block type="lists_length"></block>' +
        '<block type="lists_isEmpty"></block>' +
        '<block type="lists_indexOf"></block>' +
        '<block type="lists_getIndex"></block>' +
        '<block type="lists_setIndex"></block>' +
        '</category>',

    'list_repeat':'<block type="lists_repeat">' +
        '<value name="NUM">' +
        '<block type="math_number">' +
        '<field name="NUM">5</field>' +
        '</block>' +
        '</value>' +
        '</block>' 
});
