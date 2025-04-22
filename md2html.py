import markdown
import sys
from pathlib import Path

def md_to_html_with_sticky_header(md_path, html_path):
    # 读取 Markdown 内容
    md_text = Path(md_path).read_text(encoding='utf-8')

    # 转换为 HTML，启用表格扩展
    html_body = markdown.markdown(md_text, extensions=['tables'])

    # 定义 CSS 样式，实现表头固定
    css = '''
    <style>
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
    }
    .table-container {
        height: 100vh;
        overflow: auto;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        table-layout: fixed;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: left;
        word-wrap: break-word;
    }
    thead th {
        position: sticky;
        top: 0;
        background-color: #f9f9f9;
        z-index: 1;
    }
    </style>
    '''

    # 构建完整的 HTML 页面
    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        {css}
    </head>
    <body>
        <div class="table-container">
            {html_body}
        </div>
    </body>
    </html>
    '''

    # 写入 HTML 文件
    Path(html_path).write_text(full_html, encoding='utf-8')
    print(f"转换完成：{html_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python md2html.py 输入文件.md 输出文件.html")
    else:
        md_to_html_with_sticky_header(sys.argv[1], sys.argv[2])
