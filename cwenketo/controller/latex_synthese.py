LATEX = r"""\documentclass{{article}}
\usepackage[legalpaper, portrait, margin=0.3in]{{geometry}}
\usepackage{{graphicx}}  

\title{{Synthèse enquête de satisfaction}}
\author{{Formation HM - Eté 2022}}
\date{{\today}}

\graphicspath{{{{{pathpics}}}}}
\begin{{document}}
\sffamily  
\maketitle
{row} 
\end{{document}}"""

LATEX_ROW = r"""\section*{{\large{{{categorie} : Note {note}/10}}}}
\begin{{minipage}}{{0.3\linewidth}}
    \centering
    \includegraphics[width=\linewidth]{{{pic_note}}}
\end{{minipage}}
\begin{{minipage}}{{0.60\linewidth}}
    \centering
    \includegraphics[width=\linewidth]{{{pic_cloud}}}
\end{{minipage}}
\vspace{{10pt}}
\subsection*{{Commentaires}}
{commentaires}"""

LATEX_COM = r""" \begin{{itemize}}
{item}
\end{{itemize}}"""

