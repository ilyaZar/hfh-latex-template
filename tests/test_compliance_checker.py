#!/usr/bin/env python3
"""Regressionstests für den statischen Tabelle-1-Compliance-Checker."""

from __future__ import annotations

import unittest

from check_compliance import audit_text


PREAMBLE = r"""
\counterwithout{footnote}{chapter}
\counterwithout{table}{chapter}
\counterwithout{figure}{chapter}
"""


class ComplianceCheckerTest(unittest.TestCase):
    def test_compliant_fixture_passes(self) -> None:
        source = (
            PREAMBLE
            + r"""
Text mit Note.\footnote{Diese Fußnote ist korrekt.}
Tabelle~\ref{tab:ok} und Abbildung~\ref{fig:ok}.
\begin{hfhtable}
  \caption{Korrekte Tabelle}
  \label{tab:ok}
  \source{Eigene Darstellung.}
\end{hfhtable}
\begin{hfhfigure}
  \caption{Korrekte Abbildung}
  \label{fig:ok}
  \source{Eigene Darstellung.}
\end{hfhfigure}
\begin{hfhsourceentries}
  \hfhsourceentry{Adler, Beate: Erster Eintrag.}
  \hfhsourceentry{Zimmer, Anton: Zweiter Eintrag.}
\end{hfhsourceentries}
"""
        )
        self.assertEqual(audit_text(source), [])

    def test_obvious_violations_are_reported(self) -> None:
        source = (
            PREAMBLE
            + r"""
Text mit Note.\footnote{diese Fußnote ist fehlerhaft}
\begin{hfhtable}
  \label{tab:missing}
\end{hfhtable}
\begin{hfhfigure}
\end{hfhfigure}
\begin{hfhsourceentries}
  \hfhsourceentry{Zimmer, Anton: Zweiter Eintrag.}
  \hfhsourceentry{Adler, Beate: Erster Eintrag.}
\end{hfhsourceentries}
"""
        )
        codes = {issue.code for issue in audit_text(source)}
        self.assertTrue(
            {"E.6", "E.7", "F.1", "F.4", "G.1", "G.5", "I.4"}
            <= codes
        )

    def test_commented_examples_are_ignored(self) -> None:
        source = (
            PREAMBLE
            + r"""
% \footnote{klein und ohne Punkt}
% \begin{hfhtable}
% \end{hfhtable}
"""
        )
        self.assertEqual(audit_text(source), [])

    def test_environment_definitions_are_not_linted_as_content(self) -> None:
        source = (
            PREAMBLE
            + r"""
\newenvironment{hfhtable}[1][htbp]
  {\begin{table}[#1]}
  {\end{table}}
\newenvironment{hfhfigure}
  {\begin{figure}}
  {\end{figure}}
"""
        )
        self.assertEqual(audit_text(source), [])

    def test_reference_inside_float_is_not_running_text(self) -> None:
        source = (
            PREAMBLE
            + r"""
\begin{hfhtable}
  \caption{Selbstverweis auf Tabelle~\ref{tab:self}}
  \label{tab:self}
  \source{Eigene Darstellung.}
\end{hfhtable}
"""
        )
        codes = {issue.code for issue in audit_text(source)}
        self.assertIn("F.4", codes)


if __name__ == "__main__":
    unittest.main()
