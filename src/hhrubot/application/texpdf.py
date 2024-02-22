from pylatex import NoEscape, Package, Document
from pylatex.base_classes import Options
from datetime import date
import re


prefix = r'''%-------------------------
% Resume in Latex
% Author : Jake Gutierrez
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

% \renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''


def generate_header(first_name, last_name, contact, site, **kwargs):
    result = ''
    result += r'\begin{center}' + '\n'
    result += fr'\textbf{{\Huge \scshape {first_name} {last_name}}} \\ \vspace{{1pt}}' + '\n'
    contacts = ''
    phone = list(filter(lambda x: x['type']['id'] == 'cell', contact))
    if phone:
        phone = phone[0]['value']['formatted']
        contacts += rf'\small {phone}'
    email = list(filter(lambda x: x['type']['id'] == 'email', contact))
    if email:
        email = email[0]['value']
        if contacts:
            contacts += r' $|$ '
        contacts += fr'\href{{mailto:{email}}}{{\underline{{{email}}}}}'
    if site:
        for site_obj in site:
            if contacts:
                contacts += r' $|$ '
            url = site_obj['url']
            name = url.replace('https://www.', '').replace('https://', '')
            contacts += fr'\href{{{url}}}{{\underline{{{name}}}}}'
    result += contacts
    result += '\n'
    result += r'\end{center}'
    return result


def generate_summary(skills, **kwargs):
    if not skills:
        return ''
    result = r'\section{Обо мне}' + '\n'
    result += skills
    return result


def split_experience_to_bullet_points(experience_string: str):
    points = re.split('\n{2,}', experience_string)
    if len(points) > 1:
        return [point.replace('\n', '. ') for point in points]
    return experience_string.split('\n')


def generate_experience(experience, **kwargs):
    if not experience:
        return ''
    result = rf'\section{{Опыт работы}}' + '\n'
    result += r'\resumeSubHeadingListStart'
    for work in experience:
        result += r'\resumeSubheading'
        start = date.fromisoformat(work['start']).strftime('%m.%Y')
        end = date.fromisoformat(work['end']).strftime('%m.%Y') if work['end'] else 'н.в.'
        period = start + ' — ' + end
        result += f'{{{work["position"]}}}{{{period}}}\n'
        company = work["company"]
        area = work["area"]
        if not area:
            area = ''
        else:
            area = area['name']
        result += f'{{{company}}}{{{area}}}\n'
        points = split_experience_to_bullet_points(work['description'])
        if points:
            result += r'\resumeItemListStart' + '\n'
            for point in points:
                result += fr'\resumeItem{{{point}}}' + '\n'
            result += r'\resumeItemListEnd' + '\n'

    result += r'\resumeSubHeadingListEnd'
    return result


def render(filename, resume_data):
    header = generate_header(**resume_data)
    summary = generate_summary(**resume_data)
    experience = generate_experience(**resume_data)
    doc = Document(
        'scratch',
        documentclass='article',
        document_options=['letterpaper', '11pt'],
        fontenc=None,
        lmodern=False,
        textcomp=False,
        page_numbers=False,
        inputenc='utf8x'
    )

    doc.packages.append(Package('cmap'))
    doc.packages.append(Package('latexsym'))
    doc.packages.append(Package('fullpage', options=Options('empty')))
    doc.packages.append(Package('titlesec'))
    doc.packages.append(Package('marvosym'))
    doc.packages.append(Package('color', options=Options('usenames', 'dvipsnames')))
    doc.packages.append(Package('verbatim'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('hyperref', options=Options('hidelinks')))
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('babel', options=Options('english', 'russian')))
    doc.packages.append(Package('tabularx'))
    # doc.packages.append(Package('lmodern'))
    doc.preamble.append(NoEscape(prefix))
    doc.append(NoEscape(header.replace('&', r'\&')))
    doc.append(NoEscape(summary.replace('&', r'\&')))
    doc.append(NoEscape(experience.replace('&', r'\&')))

    doc.generate_tex(filename)
    doc.generate_pdf(filename, clean_tex=False)
