try:
    import markdown
    from fpdf import FPDF
except ModuleNotFoundError as error:
    missing_module = getattr(error, 'name', None) or str(error)
    print(f"Erro: módulo Python não encontrado: {missing_module}")
    print("Instale as dependências com: python -m pip install markdown fpdf")
    raise SystemExit(1)


def markdown_to_pdf(input_path: str, output_path: str) -> None:
    with open(input_path, encoding='utf-8') as md_file:
        html_text = markdown.markdown(md_file.read())

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', size=11)

    # Convert HTML to plain text lines for PDF output
    text_lines = html_text.replace('<h1>', '\n').replace('</h1>', '\n')
    text_lines = text_lines.replace('<code>', '``').replace('</code>', '``')
    text_lines = text_lines.replace('<pre>', '\n').replace('</pre>', '\n')
    text_lines = text_lines.replace('<strong>', '').replace('</strong>', '')
    text_lines = text_lines.replace('<em>', '').replace('</em>', '')
    text_lines = text_lines.replace('<p>', '').replace('</p>', '\n')
    text_lines = text_lines.replace('<br />', '\n')
    for line in text_lines.split('\n'):
        line = line.strip()
        if line:
            pdf.multi_cell(0, 8, line)

    pdf.output(output_path)


def main() -> None:
    markdown_to_pdf('report.md', 'report.pdf')
    print('Relatório PDF gerado como report.pdf')


if __name__ == '__main__':
    main()
