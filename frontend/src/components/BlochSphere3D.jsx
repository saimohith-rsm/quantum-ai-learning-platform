import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { useQuantum } from '../context/QuantumContext';

export default function BlochSphere3D() {
  const containerRef = useRef(null);
  const { circuit, selectedQubit, setSelectedQubit, currentStepData } = useQuantum();

  const stepData = currentStepData();
  const blochVectors = stepData?.bloch_vectors || [];
  const currentVector = blochVectors.find(v => v.qubit === selectedQubit) || {
    x: 0, y: 0, z: 1, purity: 1.0, theta_rad: 0, phi_rad: 0
  };

  const sceneRef = useRef(null);
  const arrowRef = useRef(null);
  const pointRef = useRef(null);
  const projLineRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const width = container.clientWidth || 320;
    const height = 300;

    // 1. Scene & Camera
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(2.2, 1.8, 2.5);
    camera.lookAt(0, 0, 0);

    // 2. Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // 3. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0x06b6d4, 1.2);
    dirLight.position.set(5, 5, 5);
    scene.add(dirLight);

    // 4. Bloch Sphere Geometry
    const radius = 1.0;
    const sphereGeo = new THREE.SphereGeometry(radius, 32, 32);
    const sphereMat = new THREE.MeshPhongMaterial({
      color: 0x0f1c3f,
      transparent: true,
      opacity: 0.35,
      wireframe: false,
      shininess: 40
    });
    const sphere = new THREE.Mesh(sphereGeo, sphereMat);
    scene.add(sphere);

    // Wireframe overlay
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0x1e3a8a,
      wireframe: true,
      transparent: true,
      opacity: 0.25
    });
    const wireSphere = new THREE.Mesh(sphereGeo, wireMat);
    scene.add(wireSphere);

    // Equator & Meridian Rings
    const ringMat = new THREE.LineBasicMaterial({ color: 0x06b6d4, transparent: true, opacity: 0.5 });
    
    // Equator (XY plane, z=0)
    const equatorGeo = new THREE.BufferGeometry();
    const eqPts = [];
    for (let i = 0; i <= 64; i++) {
      const a = (i / 64) * Math.PI * 2;
      eqPts.push(new THREE.Vector3(Math.cos(a), 0, Math.sin(a)));
    }
    equatorGeo.setFromPoints(eqPts);
    scene.add(new THREE.Line(equatorGeo, ringMat));

    // Axes lines: Three.js Y is Up. In standard Bloch sphere, Z is up (+|0> at top, -|1> at bottom).
    // Mapping: Three.js Y = Quantum Z, Three.js X = Quantum X, Three.js Z = Quantum Y
    const axisMat = new THREE.LineBasicMaterial({ color: 0x64748b, transparent: true, opacity: 0.4 });
    const zAxisGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, -1.3, 0), new THREE.Vector3(0, 1.3, 0)
    ]);
    scene.add(new THREE.Line(zAxisGeo, axisMat));

    const xAxisGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-1.3, 0, 0), new THREE.Vector3(1.3, 0, 0)
    ]);
    scene.add(new THREE.Line(xAxisGeo, axisMat));

    const yAxisGeo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, -1.3), new THREE.Vector3(0, 0, 1.3)
    ]);
    scene.add(new THREE.Line(yAxisGeo, axisMat));

    // 5. State Vector Arrow
    // Mapping quantum (x, y, z) to Three.js (x, z_up, y)
    const qx = currentVector.x;
    const qy = currentVector.y;
    const qz = currentVector.z;
    const dir = new THREE.Vector3(qx, qz, qy); // Three.js Y is up
    const len = Math.max(0.01, dir.length());
    dir.normalize();

    const arrow = new THREE.ArrowHelper(dir, new THREE.Vector3(0, 0, 0), len, 0x06b6d4, 0.18, 0.1);
    scene.add(arrow);
    arrowRef.current = arrow;

    // Tip dot
    const tipGeo = new THREE.SphereGeometry(0.04, 16, 16);
    const tipMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
    const tipMesh = new THREE.Mesh(tipGeo, tipMat);
    tipMesh.position.set(qx, qz, qy);
    scene.add(tipMesh);
    pointRef.current = tipMesh;

    // 6. Interactive Mouse Orbit Dragging
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    let sphericalTheta = Math.PI / 4;
    let sphericalPhi = Math.PI / 4;
    const dist = 3.2;

    const updateCameraPos = () => {
      camera.position.x = dist * Math.sin(sphericalTheta) * Math.cos(sphericalPhi);
      camera.position.y = dist * Math.cos(sphericalTheta);
      camera.position.z = dist * Math.sin(sphericalTheta) * Math.sin(sphericalPhi);
      camera.lookAt(0, 0, 0);
    };
    updateCameraPos();

    const onMouseDown = (e) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseMove = (e) => {
      if (!isDragging) return;
      const dx = e.clientX - prevMouseX;
      const dy = e.clientY - prevMouseY;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;

      sphericalPhi -= dx * 0.01;
      sphericalTheta = Math.max(0.1, Math.min(Math.PI - 0.1, sphericalTheta - dy * 0.01));
      updateCameraPos();
    };

    const onMouseUp = () => { isDragging = false; };

    container.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // Animation Loop
    let animId;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animId);
      container.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      renderer.dispose();
    };
  }, []);

  // Update arrow whenever currentVector or selectedQubit changes
  useEffect(() => {
    if (!arrowRef.current || !pointRef.current) return;
    const qx = currentVector.x;
    const qy = currentVector.y;
    const qz = currentVector.z;

    const dir = new THREE.Vector3(qx, qz, qy);
    const len = Math.max(0.01, dir.length());
    dir.normalize();

    arrowRef.current.setDirection(dir);
    arrowRef.current.setLength(len, 0.18, 0.1);
    pointRef.current.position.set(qx, qz, qy);
  }, [currentVector, selectedQubit]);

  const isPure = currentVector.purity > 0.95;

  return (
    <div className="bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-4 flex flex-col shadow-xl">
      {/* Header with Qubit Selector */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <span>3D Bloch Sphere</span>
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono">
              Qubit {selectedQubit}
            </span>
          </h3>
          <p className="text-[11px] text-slate-400">Drag to rotate view in 3D</p>
        </div>

        {/* Qubit pills */}
        <div className="flex items-center gap-1">
          {Array.from({ length: circuit.qubits }).map((_, qIdx) => (
            <button
              key={qIdx}
              onClick={() => setSelectedQubit(qIdx)}
              className={`px-2 py-1 text-xs font-mono rounded-lg transition ${
                selectedQubit === qIdx
                  ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/30'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              q[{qIdx}]
            </button>
          ))}
        </div>
      </div>

      {/* 3D Canvas Viewport */}
      <div className="relative h-[240px] flex items-center justify-center cursor-grab active:cursor-grabbing">
        <div ref={containerRef} className="w-full h-full" />
        
        {/* Pole indicators overlay */}
        <div className="absolute top-2 left-1/2 -translate-x-1/2 text-[10px] font-mono font-bold text-cyan-300 bg-slate-900/80 px-2 py-0.5 rounded border border-cyan-500/30">
          |0⟩ (North)
        </div>
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[10px] font-mono font-bold text-purple-300 bg-slate-900/80 px-2 py-0.5 rounded border border-purple-500/30">
          |1⟩ (South)
        </div>
      </div>

      {/* Numerical Coordinates & Purity */}
      <div className="pt-2 border-t border-slate-800 grid grid-cols-4 gap-2 text-center text-xs font-mono">
        <div className="p-1.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
          <div className="text-[10px] text-slate-400">x</div>
          <div className="text-cyan-400 font-bold">{currentVector.x.toFixed(3)}</div>
        </div>
        <div className="p-1.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
          <div className="text-[10px] text-slate-400">y</div>
          <div className="text-cyan-400 font-bold">{currentVector.y.toFixed(3)}</div>
        </div>
        <div className="p-1.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
          <div className="text-[10px] text-slate-400">z</div>
          <div className="text-cyan-400 font-bold">{currentVector.z.toFixed(3)}</div>
        </div>
        <div className="p-1.5 rounded-lg bg-slate-900/50 border border-slate-800/80">
          <div className="text-[10px] text-slate-400">Purity</div>
          <div className={`font-bold ${isPure ? 'text-emerald-400' : 'text-amber-400'}`}>
            {(currentVector.purity * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {!isPure && (
        <div className="mt-2 text-[11px] p-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 flex items-center gap-1.5">
          <span>⚠️ Reduced purity: Qubit {selectedQubit} is entangled with another qubit!</span>
        </div>
      )}
    </div>
  );
}
