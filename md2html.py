import markdown
import sys
from pathlib import Path
from bs4 import BeautifulSoup

def md_to_html_with_column_toggle(md_path, html_path):
    # 读取 Markdown 内容
    md_text = Path(md_path).read_text(encoding='utf-8')

    # 转换为 HTML，启用表格扩展
    html_body = markdown.markdown(md_text, extensions=['tables'])

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_body, 'html.parser')

    # 查找第一个表格
    table = soup.find('table')
    if not table:
        print("未找到表格。")
        return

    # 获取表头
    thead = table.find('thead')
    if not thead:
        # 如果没有 thead，尝试从第一个 tr 中提取 th
        first_tr = table.find('tr')
        if not first_tr:
            print("表格中未找到行。")
            return
        headers = first_tr.find_all(['th', 'td'])
        thead = soup.new_tag('thead')
        thead.append(first_tr)
        table.insert(0, thead)
    else:
        headers = thead.find_all('th')

    # 为每列添加类名
    for idx, th in enumerate(headers):
        col_class = f'col-{idx}'
        th['class'] = th.get('class', []) + [col_class]
        # 为每一行的对应列添加相同的类名
        for tr in table.find_all('tr'):
            tds = tr.find_all(['td', 'th'])
            if len(tds) > idx:
                tds[idx]['class'] = tds[idx].get('class', []) + [col_class]

    # 创建复选框控制面板
    control_div = soup.new_tag('div', **{'id': 'column-controls'})
    for idx, th in enumerate(headers):
        col_class = f'col-{idx}'
        label = soup.new_tag('label')
        checkbox = soup.new_tag('input', type='checkbox', checked='checked', **{'data-col': col_class})
        label.append(checkbox)
        label.append(f' {th.get_text()} ')
        control_div.append(label)

    # 插入控制面板到 body 前
    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
            }}
            #column-controls {{
                padding: 10px;
                background-color: #f0f0f0;
                position: sticky;
                top: 0;
                z-index: 2;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
                word-wrap: break-word;
            }}
            thead th {{
                position: sticky;
                top: 40px;
                background-color: #f9f9f9;
                z-index: 1;
            }}
        </style>
    </head>
    <body>
        {str(control_div)}
        {str(soup)}
        <script>
            document.querySelectorAll('#column-controls input[type="checkbox"]').forEach(function(checkbox) {{
                checkbox.addEventListener('change', function() {{
                    var colClass = this.getAttribute('data-col');
                    var cells = document.querySelectorAll('.' + colClass);
                    cells.forEach(function(cell) {{
                        cell.style.display = checkbox.checked ? '' : 'none';
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    '''

    # 写入 HTML 文件
    Path(html_path).write_text(full_html, encoding='utf-8')
    print(f"转换完成：{html_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python md2html_toggle.py 输入文件.md 输出文件.html")
    else:
        md_to_html_with_column_toggle(sys.argv[1], sys.argv[2])
