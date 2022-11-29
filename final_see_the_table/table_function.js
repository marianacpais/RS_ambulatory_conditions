$(document).ready(function () {
    var table = $('#example').DataTable({
        order: [[10, 'asc']],
        orderFixed: [[14, 'asc']],
        rowGroup: {
            dataSrc: 14
        },
        columnDefs: [
            {
                target: 0,
                visible: false,
                searchable: false,
            },
            {
                target: 1,
                visible: false,
                searchable: false,
            },
            {
                target: 2,
                visible: false,
            },
            {
                target: 3,
                visible: true,
            },
            {
                target: 4,
                visible: false,
            },
            {
                target: 5,
                visible: true,
            },
            {
                target: 6,
                visible: true,
            },
            {
                target: 7,
                visible: false,
            },
            {
                target: 8,
                visible: false,
            },
            {
                target: 9,
                visible: false,
            },
            {
                target: 10,
                visible: true,
            },
            {
                target: 11,
                visible: false,
            },
            {
                target: 12,
                visible: false,
            },
            {
                target: 13,
                visible: false,
            },
            {
                target: 14,
                visible: false,
            }
        ],
    });
 
});

// 1"id":1
// 2"original_description":"Intestinal infectious diseases"
// V 3"code":"A09.0"
// 4"nearest_level1_code":"A09"
// V 5"original_code_system":"ICD10"
// V 6"article":"Schuettig et al (2019)"
// 7"code_description":"ERROR"
// 8"level1_code_description":"Infectious gastroenteritis and colitis, unspecified"
// 9"extra_code_description":null
// V 10"code_description_consolidated":"Infectious gastroenteritis and colitis, unspecified"
// 11"level1_code_description_consolidated":"Infectious gastroenteritis and colitis, unspecified"
// 12"parent_ui":"A00-A09"
// 13"parent_description":"Intestinal infectious diseases (A00-A09)"
// GROUP 14"major_grouping_variable":"Intestinal infectious diseases"