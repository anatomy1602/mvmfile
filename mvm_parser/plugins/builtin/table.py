from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class TablePlugin(ComponentPlugin):
    name = "table"

    def render(self, section: "DataObject", children: list) -> str:
        columns = section.get("columns", [])
        rows = section.get("rows", [])
        caption = section.get("caption", "")
        sortable = section.get("sortable", False)

        html = '<div class="mvm-table-container">'
        if caption:
            html += f'<div class="mvm-table-caption">{caption}</div>'
        
        table_class = "mvm-table-sortable" if sortable else "mvm-table"
        html += f'<table class="{table_class}">'
        
        html += '<thead><tr>'
        for col in columns:
            label = col.get("label", "")
            key = col.get("key", "")
            if sortable:
                html += f'<th onclick="sortTable(this, \'{key}\')">{label} <span class="sort-icon">↕</span></th>'
            else:
                html += f'<th>{label}</th>'
        html += '</tr></thead>'
        
        html += '<tbody>'
        for row in rows:
            highlight = row.get("highlight", False)
            row_class = "mvm-table-row-highlight" if highlight else ""
            html += f'<tr class="{row_class}">'
            for col in columns:
                key = col.get("key", "")
                value = row.get(key, "")
                html += f'<td>{value}</td>'
            html += '</tr>'
        html += '</tbody>'
        
        html += '</table></div>'
        return html

    def get_css(self) -> str:
        return """
.mvm-table-container {
    margin: 1em 0;
    overflow-x: auto;
}
.mvm-table-caption {
    font-weight: bold;
    margin-bottom: 0.5em;
    color: var(--text-primary);
}
.mvm-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-primary);
}
.mvm-table th, .mvm-table td {
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
}
.mvm-table th {
    background: var(--bg-secondary);
    font-weight: bold;
    color: var(--text-primary);
}
.mvm-table tr:hover {
    background: var(--bg-hover);
}
.mvm-table-row-highlight {
    background: var(--accent-light);
}
.mvm-table-sortable th {
    cursor: pointer;
    user-select: none;
}
.mvm-table-sortable th:hover {
    background: var(--bg-hover);
}
.sort-icon {
    font-size: 0.8em;
    margin-left: 4px;
    opacity: 0.5;
}
"""

    def get_js(self) -> str:
        return """
let currentSortColumn = null;
let currentSortDirection = 'asc';

function sortTable(th, key) {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    if (currentSortColumn === key) {
        currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortColumn = key;
        currentSortDirection = 'asc';
    }
    
    rows.sort((a, b) => {
        const aVal = a.querySelector(`td:nth-child(${Array.from(th.parentNode.children).indexOf(th) + 1})`).textContent.trim();
        const bVal = b.querySelector(`td:nth-child(${Array.from(th.parentNode.children).indexOf(th) + 1})`).textContent.trim();
        
        const aNum = parseFloat(aVal);
        const bNum = parseFloat(bVal);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return currentSortDirection === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        return currentSortDirection === 'asc' 
            ? aVal.localeCompare(bVal) 
            : bVal.localeCompare(aVal);
    });
    
    rows.forEach(row => tbody.appendChild(row));
    
    document.querySelectorAll('.sort-icon').forEach(icon => {
        icon.textContent = '↕';
        icon.style.opacity = '0.5';
    });
    
    const icon = th.querySelector('.sort-icon');
    icon.textContent = currentSortDirection === 'asc' ? '↑' : '↓';
    icon.style.opacity = '1';
}
"""
