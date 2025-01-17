\version "2.24.4"
\language "english"
\score
{
    % OPEN_BRACKETS:
    \new Score
    <<
        % OPEN_BRACKETS:
        \context Devnull = "MetricStaff"
        {
            % BEFORE:
            % COMMANDS:
            \tempo 4=135
            s1
        % CLOSE_BRACKETS:
        }
        % OPEN_BRACKETS:
        \context Staff = "ariel_lpf"
        \with
        {
            instrumentName = "ariel_lpf"
            shortInstrumentName = "ar."
            %{
            ---CSOUND INFO---
            Instrument = ariel_lpf
            Channels = 1
            %}
        }
        {
            af''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            b'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            af''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            a'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            bf'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            d''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            e'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            bf''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            cs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            bf''16
            % AFTER:
            % ARTICULATIONS:
            \p
            bf'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            fs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            bf''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            g'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            d'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            d'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            bf'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            f'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            d''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            e'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            cs'16
            % AFTER:
            % ARTICULATIONS:
            \p
            g'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            ef'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            f''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            bf'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            cs'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            cs'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            g'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            a''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            d'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            c'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            f''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            e'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            b'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            e'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            af'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            d''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a''16
            % AFTER:
            % ARTICULATIONS:
            \p
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            bf''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            b'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            d''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            d''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            af'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            af'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            bf''16
            % AFTER:
            % ARTICULATIONS:
            \p
            g'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            a''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            b'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            c''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            d'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            e''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            a''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            g'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            f'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            a'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            af''16
            % AFTER:
            % ARTICULATIONS:
            \p
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            b'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            f''16
            % AFTER:
            % ARTICULATIONS:
            \p
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            d''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            f'16
            % AFTER:
            % ARTICULATIONS:
            \p
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            b''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            g'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            af'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            c''''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            a'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            fs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            g'16
            % AFTER:
            % ARTICULATIONS:
            \p
            a'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            e''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            g''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            e'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            bf'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            fs''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            b'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            c''''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            g'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            a'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            b'16
            % AFTER:
            % ARTICULATIONS:
            \p
            d'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            b'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            d''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs'16
            % AFTER:
            % ARTICULATIONS:
            \p
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            f''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            b''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            a''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a''16
            % AFTER:
            % ARTICULATIONS:
            \p
            g''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            c'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            b''16
            % AFTER:
            % ARTICULATIONS:
            \p
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            f''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            b'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            g'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            d''16
            % AFTER:
            % ARTICULATIONS:
            \p
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            c''''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            b''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \p
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            ef'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            f''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            c''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            af''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            ef'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            g'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            e'16
            % AFTER:
            % ARTICULATIONS:
            \p
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            b'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            af'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            b'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            bf'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            bf'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            af'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            g'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            b'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            af'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            c''''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            bf'16
            % AFTER:
            % ARTICULATIONS:
            \p
            cs'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            c'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            g'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \p
            af''16
            % AFTER:
            % ARTICULATIONS:
            \p
            c''''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            ef'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            g'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            c''''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            g'16
            % AFTER:
            % ARTICULATIONS:
            \p
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            f'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            b'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            e''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            fs'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            g''16
            % AFTER:
            % ARTICULATIONS:
            \p
            bf'16
            % AFTER:
            % ARTICULATIONS:
            \p
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            b'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            af'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            e'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            cs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            bf''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            d''16
            % AFTER:
            % ARTICULATIONS:
            \p
            g'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            ef''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            ef'16
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            e'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c''16
            % AFTER:
            % ARTICULATIONS:
            \p
            a'16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            g'16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            fs'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            d'''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            f''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \fff
            g'''16
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            fs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            c''16
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs''16
            % AFTER:
            % ARTICULATIONS:
            \p
            c'''16
            % AFTER:
            % ARTICULATIONS:
            \p
        % CLOSE_BRACKETS:
        }
        % OPEN_BRACKETS:
        \context Staff = "ariel_1"
        \with
        {
            instrumentName = "ariel"
            shortInstrumentName = "ar."
            %{
            ---CSOUND INFO---
            Instrument = ariel
            Channels = 2
            %}
        }
        {
            % OPENING:
            % COMMANDS:
            \clef "bass"
            fs,,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            g4
            % AFTER:
            % ARTICULATIONS:
            \fff
            f,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            b4
            % AFTER:
            % ARTICULATIONS:
            \p
            b4
            % AFTER:
            % ARTICULATIONS:
            \p
            c4
            % AFTER:
            % ARTICULATIONS:
            \mf
            e,,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            g4
            % AFTER:
            % ARTICULATIONS:
            \fff
            ef,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            e,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            cs,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            fs4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            fs,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            g4
            % AFTER:
            % ARTICULATIONS:
            \fff
            f4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            g,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            ef,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            b,,4
            % AFTER:
            % ARTICULATIONS:
            \p
            ef4
            % AFTER:
            % ARTICULATIONS:
            \fff
            ef4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            e,,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            e4
            % AFTER:
            % ARTICULATIONS:
            \p
            e,,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            af,,4
            % AFTER:
            % ARTICULATIONS:
            \p
            a4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a4
            % AFTER:
            % ARTICULATIONS:
            \p
            c4
            % AFTER:
            % ARTICULATIONS:
            \p
            ef4
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            b,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            g4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            d4
            % AFTER:
            % ARTICULATIONS:
            \p
            g,,4
            % AFTER:
            % ARTICULATIONS:
            \p
            fs4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            f,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            af4
            % AFTER:
            % ARTICULATIONS:
            \p
            d,4
            % AFTER:
            % ARTICULATIONS:
            \p
            bf,,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            ef,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            cs,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            af,,4
            % AFTER:
            % ARTICULATIONS:
            \p
            af,,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            f,,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            ef4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            a,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            c'4
            % AFTER:
            % ARTICULATIONS:
            \p
            d,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            f,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            af,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            f,,4
            % AFTER:
            % ARTICULATIONS:
            \p
            af,,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            c4
            % AFTER:
            % ARTICULATIONS:
            \mf
            b4
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            d,4
            % AFTER:
            % ARTICULATIONS:
            \p
            a,4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            d,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            e4
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            a,,4
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            a,,4
            % AFTER:
            % ARTICULATIONS:
            \mf
            g4
            % AFTER:
            % ARTICULATIONS:
            \fff
            e,,4
            % AFTER:
            % ARTICULATIONS:
            \mf
        % CLOSE_BRACKETS:
        }
        % OPEN_BRACKETS:
        \context Staff = "ariel_2"
        \with
        {
            instrumentName = "ariel"
            shortInstrumentName = "ar."
            %{
            ---CSOUND INFO---
            Instrument = ariel
            Channels = 2
            %}
        }
        {
            % OPENING:
            % COMMANDS:
            \clef "bass"
            cs2
            % AFTER:
            % ARTICULATIONS:
            \fff
            f,,2
            % AFTER:
            % ARTICULATIONS:
            \mf
            cs,2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            e2
            % AFTER:
            % ARTICULATIONS:
            \p
            bf,,2
            % AFTER:
            % ARTICULATIONS:
            \mf
            b,,2
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            g2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            f2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            c2
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a,,2
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            bf,2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            a,,2
            % AFTER:
            % ARTICULATIONS:
            \fff
            c,2
            % AFTER:
            % ARTICULATIONS:
            \p
            ef2
            % AFTER:
            % ARTICULATIONS:
            \fff
            b2
            % AFTER:
            % ARTICULATIONS:
            \mf
            b2
            % AFTER:
            % ARTICULATIONS:
            \fff
            ef2
            % AFTER:
            % ARTICULATIONS:
            \mf
            f,2
            % AFTER:
            % ARTICULATIONS:
            \mf
            b,,2
            % AFTER:
            % ARTICULATIONS:
            \fff
            c'2
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            e,,2
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            af2
            % AFTER:
            % ARTICULATIONS:
            \fff
            % SPANNER_STARTS:
            \glissando
            c,2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            af2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            g,,2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            f2
            % AFTER:
            % ARTICULATIONS:
            \fff
            cs2
            % AFTER:
            % ARTICULATIONS:
            \fff
            e2
            % AFTER:
            % ARTICULATIONS:
            \mf
            % SPANNER_STARTS:
            \glissando
            a2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            c'2
            % AFTER:
            % ARTICULATIONS:
            \fff
            fs,,2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
            cs2
            % AFTER:
            % ARTICULATIONS:
            \p
            % SPANNER_STARTS:
            \glissando
        % CLOSE_BRACKETS:
        }
    % CLOSE_BRACKETS:
    >>
}
