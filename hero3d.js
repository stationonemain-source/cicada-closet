// The Cicada Closet — hero.
//
// Her logo, flat, printed flush on kraft paper. No sculpted relief: a generated mesh gave the
// artwork depth but cost it its edges, and her linework is the point. The only 3D here is the
// camera — a real perspective push toward the keyhole and through it, so the sheet spreads past
// the frame and you see into the hole. Every visible pixel is her own file.
import * as THREE from 'three';

const host = document.getElementById('stage3d');
if (host) {
  const KY = 0.3665;                       // keyhole centre, as a fraction of the logo
  const PAPER = 3.0;                       // paper size in world units
  const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = Math.min(innerWidth, innerHeight) < 700 || (devicePixelRatio || 1) < 1.5;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.setSize(innerWidth, innerHeight);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, innerWidth / innerHeight, 0.01, 60);

  // the dark behind the keyhole: a shaft, narrower than the sheet, DoubleSide so it holds once inside
  const well = new THREE.Mesh(
    new THREE.BoxGeometry(PAPER * 0.55, PAPER * 0.55, 9),
    new THREE.MeshBasicMaterial({ color: 0x0b0806, side: THREE.DoubleSide })
  );
  well.position.z = -4.55;
  scene.add(well);

  // her sheet: the artwork itself, with the keyhole transparent so the shaft shows through
  const paper = new THREE.Mesh(
    new THREE.PlaneGeometry(PAPER, PAPER),
    new THREE.MeshBasicMaterial({ transparent: true, side: THREE.DoubleSide })
  );
  scene.add(paper);

  // the same kraft continuing past the sheet, so the surface never ends on screen
  const field = new THREE.Mesh(
    new THREE.PlaneGeometry(PAPER * 9, PAPER * 9),
    new THREE.MeshBasicMaterial({ color: 0xab7e56 })
  );
  field.position.z = -0.30;
  scene.add(field);

  const aimY = (0.5 - KY) * PAPER;
  well.position.y = aimY;

  const tl = new THREE.TextureLoader();
  tl.load(host.dataset[small ? 'art2k' : 'art4k'], (t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    // her edges are drawn, not generated: sample them properly at every angle and scale
    t.anisotropy = Math.min(16, renderer.capabilities.getMaxAnisotropy());
    t.generateMipmaps = true;
    t.minFilter = THREE.LinearMipmapLinearFilter;
    t.magFilter = THREE.LinearFilter;
    paper.material.map = t; paper.material.needsUpdate = true;
    host.dispatchEvent(new CustomEvent('hero3d:ready'));
  });
  tl.load(host.dataset.kraft, (t) => {
    t.colorSpace = THREE.SRGBColorSpace;
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(16, 16);
    field.material.map = t; field.material.color.set(0xffffff); field.material.needsUpdate = true;
  });

  let restZ = 4.35, restLift = 0, restShift = 0;
  function frame(p) {
    const e = prefersReduced ? 0 : Math.pow(p, 0.88);
    const k = Math.pow(Math.max(0, 1 - e / 0.68), 1.5);   // rest offsets are gone before the keyhole
    const lift = restLift * k, side = restShift * k;
    const z = restZ - e * (restZ + 0.70);
    camera.position.set(-side, aimY * (1 - e * 0.15) + lift, z);
    camera.lookAt(-side, aimY + lift, -1);
    paper.rotation.x = (1 - e) * 0.085;                   // the sheet leans back, then squares up
    field.rotation.x = paper.rotation.x;
    renderer.render(scene, camera);
  }

  function resize() {
    camera.aspect = innerWidth / innerHeight;
    camera.fov = camera.aspect < 0.85 ? 58 : 42;
    // wide screens put the copy in a left column (see .beat.hero), so the sheet sits to the right
    const wide = camera.aspect >= 1.25, mid = camera.aspect >= 0.85;
    restZ     = wide ? 3.80  : mid ? 4.05  : 4.35;
    restLift  = wide ? -0.30 : mid ? -0.12 : 0.08;
    restShift = wide ? 0.95  : 0;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  }
  addEventListener('resize', resize);
  resize();

  window.__hero3d = { frame, isReady: () => !!paper.material.map };
}
