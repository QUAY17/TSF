/* global React, ReactDOM, TweaksPanel, TweakSection, TweakRadio, TweakToggle, TweakButton, useTweaks */

const TSF_TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "layout": "a",
  "hero": "split",
  "density": "balanced",
  "annotate": false
}/*EDITMODE-END*/;

function TsfTweaks() {
  const [t, setTweak] = useTweaks(TSF_TWEAK_DEFAULTS);

  // Push current tweak values onto <body> data-* so CSS can react
  React.useEffect(() => {
    const b = document.body;
    b.setAttribute('data-layout',   t.layout);
    b.setAttribute('data-hero',     t.hero);
    b.setAttribute('data-density',  t.density);
    b.setAttribute('data-annotate', t.annotate ? 'on' : 'off');
  }, [t.layout, t.hero, t.density, t.annotate]);

  return (
    <TweaksPanel title="Tweaks">
      <TweakSection label="Layout variant" />
      <TweakRadio
        label="Composition"
        value={t.layout}
        options={[
          { label: 'A · Editorial', value: 'a' },
          { label: 'B · Magazine',  value: 'b' },
          { label: 'C · Archive',   value: 'c' },
        ]}
        onChange={(v) => setTweak('layout', v)}
      />

      <TweakSection label="Hero style" />
      <TweakRadio
        label="Hero"
        value={t.hero}
        options={[
          { label: 'Bleed',  value: 'bleed' },
          { label: 'Split',  value: 'split' },
          { label: 'Type',   value: 'type'  },
        ]}
        onChange={(v) => setTweak('hero', v)}
      />

      <TweakSection label="Density" />
      <TweakRadio
        label="Spacing"
        value={t.density}
        options={[
          { label: 'Airy',     value: 'airy'     },
          { label: 'Balanced', value: 'balanced' },
          { label: 'Compact',  value: 'compact'  },
        ]}
        onChange={(v) => setTweak('density', v)}
      />

      <TweakSection label="Reference" />
      <TweakToggle
        label="Show Squarespace mapping"
        value={t.annotate}
        onChange={(v) => setTweak('annotate', v)}
      />
    </TweaksPanel>
  );
}

// Mount panel + apply defaults immediately so first paint is correct
(function bootTweaks() {
  const b = document.body;
  b.setAttribute('data-layout',   TSF_TWEAK_DEFAULTS.layout);
  b.setAttribute('data-hero',     TSF_TWEAK_DEFAULTS.hero);
  b.setAttribute('data-density',  TSF_TWEAK_DEFAULTS.density);
  b.setAttribute('data-annotate', TSF_TWEAK_DEFAULTS.annotate ? 'on' : 'off');

  const mount = document.createElement('div');
  mount.id = 'tsf-tweaks-mount';
  document.body.appendChild(mount);
  ReactDOM.createRoot(mount).render(<TsfTweaks />);
})();
