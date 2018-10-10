\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{odgdoc}[2017/03/14 ODG Document]

\LoadClass{article}

% \usepackage{lmodern}
%% fonts

\usepackage{anyfontsize}
\usepackage[usenames,dvipsnames]{color}
\usepackage{geometry}
\geometry{verbose,tmargin=1.5in,bmargin=1.5in,lmargin=1.5in,rmargin=1.5in}
\usepackage{tikz}
\usetikzlibrary{positioning}
\usepackage{fancyhdr}
\usepackage{sectsty}

%% colors
\definecolor{titlegray}{RGB}{71, 72, 69}
\definecolor{pagenum}{RGB}{71, 72, 69}
\definecolor{headrule}{RGB}{196, 197, 195}
\definecolor{header}{RGB}{71, 72, 69}
\definecolor{sectionfont}{RGB}{71, 72, 69}
\definecolor{subsectionfont}{RGB}{71, 72, 69}

% odg gray
% 71 72 69

\newcommand{\subtitle}[1]{\def\@subtitle{#1}}
\subtitle{}

\renewcommand{\maketitle}{ %

  \begin{tikzpicture}[remember picture,overlay]
    \node[opacity=1.0,inner sep=0pt] at (current page.center){\includegraphics[width=\paperwidth,height=\paperheight]{ODG_doc_frontcover}};
    \node[anchor=west, text width=0.62\paperwidth, font=\fontsize{34}{40}\selectfont] (title) at ([yshift=0.21\paperheight, xshift=-0.38\paperwidth]current page.center){\textcolor{titlegray}{\textsf{\@title}}};
    \node[below left = 1em and 0em of title, anchor=west, font=\fontsize{12}{12}\selectfont] {\textcolor{titlegray}{\textsf{\bfseries \MakeUppercase \@subtitle}}};
  \end{tikzpicture}
  \thispagestyle{empty}
  \pagebreak{}
}

%% regular pages

\pagestyle{fancy}
\lfoot{}
\rfoot{}
\cfoot{
  \begin{tikzpicture}[remember picture, overlay]
    \node[opacity=1.0,inner sep=0pt] at (current page.center){\includegraphics[width=\paperwidth,height=\paperheight]{ODG_doc_page}};
    \node at ([yshift=-0.469\paperheight, xshift=0.436\paperwidth]current page.center){\textsf{\textcolor{pagenum}{\thepage}}};
  \end{tikzpicture}
}

% Length to control the \fancyheadoffset and the calculation of \headline
% simultaneously
\newlength\FHoffset
\setlength\FHoffset{0cm}

\addtolength\headwidth{2\FHoffset}

\fancyheadoffset{\FHoffset}

% these lengths will control the headrule trimming to the left and right
\newlength\FHleft
\newlength\FHright

% here the trimmings are controlled by the user
\setlength\FHleft{-10cm}
\setlength\FHright{-10cm}

% The new definition of headrule that will take into acount the trimming(s)
\newbox\FHline
\setbox\FHline=\hbox{\hsize=\paperwidth%
  \hspace*{\FHleft}%
  {\color{headrule}
  \rule{\dimexpr\headwidth-\FHleft-\FHright\relax}{\headrulewidth}}\hspace*{\FHright}%
}
\renewcommand\headrule{\vskip-.7\baselineskip\copy\FHline}

% \fancyhead[R]{\rightmark}  % \rightmark is 3.2 Subsection
\fancyhead[R]{}
\fancyhead[C]{}
\fancyhead[L]{\textcolor{header}{\textsf{\bfseries \large \MakeUppercase \leftmark}}} % \leftmark is 3 Section

%% section styling

\allsectionsfont{\color{subsectionfont} \sffamily}
\sectionfont{\color{sectionfont} \sffamily \MakeUppercase}

% paragraph styling
\usepackage{parskip}
