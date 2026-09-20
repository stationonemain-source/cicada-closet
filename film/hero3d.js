// The Cicada Closet — 3D hero.
//
// Her logo is a texture on a plane in real space, with the keyhole punched clean through it.
// Behind it sits a dark volume. A perspective camera flies toward the keyhole and through it.
// Because it is a real camera in a real frustum, the perspective CHANGES as you move: the
// paper spreads past the edges of the screen and you see into the hole with parallax. That
// shift is what a 2D scale can never fake, and it is the whole reason this is rendered in 3D.
//
// Her artwork is a texture, pixel for pixel. Nothing about it is regenerated.
(function () {
  const host = document.getElementById('stage3d');
  if (!host || typeof THREE === 'undefined') return;

  const KY = 0.3665;                       // keyhole centre, as a fraction of the logo
  const PAPER = 3.0;                       // paper size in world units
  const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = Math.min(innerWidth, innerHeight) < 700 || (devicePixelRatio || 1) < 1.5;
  const texUrl = host.dataset[small ? 'tex2k' : 'tex4k'];

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.setSize(innerWidth, innerHeight);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, innerWidth / innerHeight, 0.01, 60);

  // The dark behind the keyhole. Deliberately SMALLER than the paper and set back from it:
  // small enough to stay hidden behind the sheet from every angle, near enough that it fills
  // the frame once the camera reaches the hole. A big box with BackSide was the first attempt
  // and it is invisible from outside -- you saw the kraft field straight through the keyhole.
  // A shaft, not a plane: its mouth sits immediately behind the sheet so it blocks the kraft
  // field showing through the hole, and DoubleSide keeps its walls drawn once the camera is
  // inside it. Narrower than the sheet's opaque area, so it never darkens the paper's edges.
  const well = new THREE.Mesh(
    new THREE.BoxGeometry(PAPER * 0.55, PAPER * 0.55, 9),
    new THREE.MeshBasicMaterial({ color: 0x0b0806, side: THREE.DoubleSide })
  );
  well.position.z = -4.55;          // mouth at -0.05, clear of the field plane
  scene.add(well);

  // the faintest warmth just inside the opening, so it reads as a room rather than a void
  const glow = new THREE.Mesh(
    new THREE.PlaneGeometry(PAPER * 0.5, PAPER * 0.5),
    new THREE.MeshBasicMaterial({ color: 0x4a3418, transparent: true, opacity: 0.0 })
  );
  glow.position.z = -1.18;
  scene.add(glow);

  // her paper
  const paper = new THREE.Mesh(
    new THREE.PlaneGeometry(PAPER, PAPER),
    new THREE.MeshBasicMaterial({ transparent: true, side: THREE.DoubleSide })
  );
  scene.add(paper);

  // the same kraft, continuing past the paper so the surface never ends on screen
  const field = new THREE.Mesh(
    new THREE.PlaneGeometry(PAPER * 9, PAPER * 9),
    new THREE.MeshBasicMaterial({ color: 0xab7e56 })
  );
  field.position.z = -0.30;         // well behind the shaft's mouth: coplanar planes z-fight,
                                    // which punched a dark bar across her artwork
  scene.add(field);

  const loader = new THREE.TextureLoader();
  let ready = false;
  loader.load(texUrl, (t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    t.generateMipmaps = true;
    t.minFilter = THREE.LinearMipmapLinearFilter;
    paper.material.map = t;
    paper.material.needsUpdate = true;
    ready = true;
    host.dispatchEvent(new CustomEvent('hero3d:ready'));
  });
  loader.load(host.dataset.kraft, (t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(16, 16);              // a 1024 seamless tile, not a 4K plate: 12x lighter, same grain
    field.material.map = t;
    field.material.color.set(0xffffff);
    field.material.needsUpdate = true;
  });

  // the keyhole sits above the paper's centre, so the camera aims there, not at the middle
  const aimY = (0.5 - KY) * PAPER;
  well.position.y = aimY;
  glow.position.y = aimY;

  function frame(p) {
    const e = prefersReduced ? 0 : Math.pow(p, 0.88);
    // the camera starts back far enough to hold the whole sheet, then flies through the keyhole;
    // wide screens start closer, or the sheet sits small in a sea of paper
    const z = restZ - e * (restZ + 0.70);
    // at rest the view is lifted so the sheet sits below the headline instead of under it;
    // the lift eases out, and by the keyhole the camera is aimed dead on it
    // rest offsets are gone by two-thirds of the way in, so the camera passes through the
    // keyhole dead centre instead of still drifting across as it arrives
    const k = Math.pow(Math.max(0, 1 - e / 0.68), 1.5);
    const lift = restLift * k;
    const side = restShift * k;            // wide screens: the sheet rests beside the text, then centres
    camera.position.set(-side, aimY * (1 - e * 0.15) + lift, z);
    camera.lookAt(-side, aimY + lift, -1);
    // the sheet leans back a touch at rest and squares up as you arrive
    paper.rotation.x = (1 - e) * 0.085;
    field.rotation.x = paper.rotation.x;
    glow.material.opacity = 0.42 * Math.min(1, Math.max(0, (e - 0.30) / 0.45));
    renderer.render(scene, camera);
  }

  let restZ = 4.35, restLift = 0, restShift = 0;
  function resize() {
    camera.aspect = innerWidth / innerHeight;
    // The camera aims at the keyhole, which sits ABOVE the sheet's centre, so with no lift the
    // sheet hangs low. Wide screens are height-bound by a square logo under a headline: pull
    // back enough for the whole sheet, and aim a little below the keyhole so it rises to sit
    // centred beneath the text. A positive lift here pushed the lettering off the bottom.
    // Wide: the headline moves to a left column (see .beat.hero in the page CSS), so the sheet
    // can take the full height on the right. Stacking text over a square logo on a wide screen
    // means either the ornament goes under the headline or the lettering goes off the bottom.
    const wide = camera.aspect >= 1.25, mid = camera.aspect >= 0.85;
    restZ     = wide ? 3.80  : mid ? 4.05  : 4.35;
    restLift  = wide ? -0.30 : mid ? -0.12 : 0.08;
    restShift = wide ? 0.95  : 0;
    // hold the whole sheet on tall screens, where a fixed fov would crop it
    camera.fov = innerWidth / innerHeight < 0.85 ? 58 : 42;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  }
  addEventListener('resize', resize);
  resize();

  window.__hero3d = { frame, isReady: () => ready };
})();
