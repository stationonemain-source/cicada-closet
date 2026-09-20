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
    t.repeat.set(3, 3);
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
    // the camera starts back far enough to hold the whole sheet, then flies through the keyhole
    const z = 4.35 - e * 5.05;
    camera.position.set(0, aimY * (1 - e * 0.15), z);
    camera.lookAt(0, aimY, -1);
    // the sheet leans back a touch at rest and squares up as you arrive
    paper.rotation.x = (1 - e) * 0.085;
    field.rotation.x = paper.rotation.x;
    glow.material.opacity = 0.42 * Math.min(1, Math.max(0, (e - 0.30) / 0.45));
    renderer.render(scene, camera);
  }

  function resize() {
    camera.aspect = innerWidth / innerHeight;
    // hold the whole sheet on tall screens, where a fixed fov would crop it
    camera.fov = innerWidth / innerHeight < 0.85 ? 58 : 42;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  }
  addEventListener('resize', resize);
  resize();

  window.__hero3d = { frame, isReady: () => ready };
})();
