// 夕焼けシグナル — Sunset Signal
// A J-pop instrumental written in Strudel · D major → E♭ major · 172 BPM
// Intro 4 · A melody 8 · B melody 8 · Chorus 8 · Break 2 · Last chorus (+1 key) 8 · Outro 4
// Paste into https://strudel.cc and press play (Ctrl+Enter).

setcpm(172 / 4)   // one cycle = one bar of 4/4

// ---------- harmony: one chord per bar, [x y] splits a bar
const H = {
  intro:  "<G A F#m Bm>",
  verse:  "<Bm G A D Bm G A A>",
  pre:    "<GM7 F#7 Bm7 [Am7 D7] GM7 F#7 Bm7 A>",   // the "Just the Two of Us" turn, then V
  chorus: "<G A F#m Bm Em A D D>",                  // 王道進行 IV–V–iii–vi
  brk:    "<A Bb>",                                 // Bb = V of E♭: the key change is coming
  outro:  "<G A D D>",
}
const ROOT = {
  intro:  "<g1 a1 f#1 b1>",
  verse:  "<b1 g1 a1 d2 b1 g1 a1 a1>",
  pre:    "<g1 f#1 b1 [a1 d2] g1 f#1 b1 a1>",
  chorus: "<g1 a1 f#1 b1 e2 a1 d2 d2>",
  brk:    "<a1 bb1>",
  outro:  "<g1 a1 d2 d2>",
}

// ---------- melody: eighth-note grid, @n holds for n eighths
const MEL = {
  verse: `<
    [~ d5 d5 c#5 d5@2 f#5 e5]  [d5@3 b4 d5 e5@2 d5]
    [c#5@2 e5 c#5 a4@2 b4 c#5] [d5@4 ~ a4 b4 c#5]
    [d5 d5 d5 c#5 d5@2 f#5 g5] [f#5@2 e5 d5 e5@2 d5 b4]
    [c#5@2 d5 e5 c#5@2 a4 c#5] [e5@6 ~ ~]>`,
  pre: `<
    [f#5@2 f#5 g5 a5@2 f#5 d5] [e5@2 e5 f#5 a#5@2 f#5 e5]
    [d5@2 c#5 d5 f#5@2 a5 f#5] [e5@2 d5 c5 d5@2 f#5 a5]
    [b5@2 a5 g5 f#5@2 e5 d5]   [c#5@2 e5 a#4 c#5@2 e5 f#5]
    [d5@2 f#5 a5 b5@2 a5 f#5]  [a5 b5 c#6 d6 e6@3 ~]>`,
  chorus: `<
    [b5@2 a5 b5 d6@2 b5 a5]    [a5@3 f#5 e5@2 c#5 e5]
    [f#5@2 e5 f#5 a5@2 c#6 a5] [b5@6 ~ ~]
    [g5@2 f#5 g5 b5@2 a5 g5]   [a5@2 g5 f#5 e5@2 d5 e5]
    [f#5@4 e5 d5 e5 f#5]       [d5@6 ~ ~]>`,
  brk:   "<~ [~@4 f5 g5 ab5 bb5]>",
  outro: "<[b5@2 a5 b5 d6@4] [c#6@2 b5 c#6 e6@4] [d6@8] ~>",
}

// ---------- instruments
const lead  = line => note(line).s("supersaw").lpf(3200).attack(.01).decay(.2).sustain(.55).release(.12)
                   .gain(.3).delay(.22).delaytime(.26).delayfeedback(.3).room(.3)
const piano = (chords, rhythm) => chord(chords).struct(rhythm).voicing().s("piano").gain(.5).room(.25)
const pad   = chords => chord(chords).voicing().s("supersaw").lpf(1500).attack(.3).release(.6).gain(.14)
const arp   = chords => chord(chords).voicing().arp("0 1 2 3 1 2 3 2 0 1 2 3 1 2 3 2")
                   .s("triangle").lpf(4000).gain(.22).delay(.2).delaytime(.26)
const bass  = roots => note(roots).struct("x*8").s("sawtooth").lpf(600).lpq(6)
                   .decay(.12).sustain(.35).gain(.55)
const dr    = hits => s(hits).bank("RolandTR909")

const DRUMS = {
  intro:  stack(dr("hh*8").gain(.3), dr("<~ ~ ~ [sd*8 sd*16]>").gain(saw.range(.3, .9))),
  verse:  stack(dr("bd ~ ~ bd ~ ~ bd ~"), dr("~ sd ~ sd"), dr("hh*8").gain(.35), dr("<cr ~ ~ ~ ~ ~ ~ ~>").gain(.6)),
  pre:    stack(dr("bd*4"), dr("~ sd ~ sd"), dr("hh*16").gain(.22), dr("<cr ~ ~ ~ cr ~ ~ ~>").gain(.6),
                dr("<~ ~ ~ ~ ~ ~ ~ [sd*8 sd*16]>").gain(saw.range(.3, 1))),
  chorus: stack(dr("bd*4"), dr("~ [sd,cp] ~ [sd,cp]"), dr("[~ oh]*4").gain(.4), dr("hh*8").gain(.22),
                dr("<cr ~ ~ ~ cr ~ ~ ~>").gain(.7)),
  brk:    dr("<[bd,cr] [lt lt mt mt ht ht [sd sd] [sd sd]]>"),
  outro:  stack(dr("<bd*4 bd*4 [bd,cr] ~>"), dr("<[~ sd ~ sd] [~ sd ~ sd] ~ ~>"), dr("<[~ oh]*4 [~ oh]*4 ~ ~>").gain(.4)),
}

// ---------- sections
const INTRO  = stack(pad(H.intro), arp(H.intro), bass(ROOT.intro).gain(.35), DRUMS.intro)
const VERSE  = stack(piano(H.verse, "x ~ ~ x ~ ~ x ~"), bass(ROOT.verse), lead(MEL.verse), DRUMS.verse)
const PRE    = stack(piano(H.pre, "x ~ x ~ x ~ x ~"), pad(H.pre), bass(ROOT.pre), lead(MEL.pre), DRUMS.pre)
const CHORUS = stack(piano(H.chorus, "x ~ x x ~ x ~ x"), pad(H.chorus), arp(H.chorus),
                     bass(ROOT.chorus), lead(MEL.chorus))
const BREAK  = stack(pad(H.brk), bass(ROOT.brk), lead(MEL.brk), DRUMS.brk)
const OUTRO  = stack(pad(H.outro), piano(H.outro, "x ~ ~ ~ ~ ~ ~ ~"), bass(ROOT.outro).struct("x ~ ~ ~ ~ ~ ~ ~"),
                     lead(MEL.outro))

arrange(
  [4, INTRO],
  [8, VERSE],
  [8, PRE],
  [8, stack(CHORUS, DRUMS.chorus)],
  [2, BREAK],
  [8, stack(CHORUS.transpose(1), DRUMS.chorus)],   // last chorus, a half step up
  [4, stack(OUTRO.transpose(1), DRUMS.outro)],
)
