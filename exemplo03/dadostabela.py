data = [{
    "name": "bootstrap-table",
    "commits": "10",
    "attention": "122",
    "uneven": "An extended Bootstrap table"
},
    {
        "name": "multiple-select",
        "commits": "288",
        "attention": "20",
        "uneven": "A jQuery plugin"
    }, {
        "name": "Testing",
        "commits": "340",
        "attention": "20",
        "uneven": "For test"
    }]
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
    {
        "field": "name",  # which is the field's name of data key
        "title": "name",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "commits",
        "title": "commits",
        "sortable": True,
    },
    {
        "field": "attention",
        "title": "attention",
        "sortable": True,
    },
    {
        "field": "uneven",
        "title": "uneven",
        "sortable": True,
    }
]
