var scene, camera, renderer;
var geometry, material, mesh;

init();
animate();

function init() {

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.z = 1;

    geometry = new THREE.SphereGeometry(250, 60, 40);
    geometry.scale(-1, 1, 1);  // 画像を内側にマッピングするためにジオメトリを反転

    // ここであなたの全天球画像をロードします
    var loader = new THREE.TextureLoader();
    material = new THREE.MeshBasicMaterial({
        map: loader.load(skyboxImageURL)
    });

    mesh = new THREE.Mesh(geometry, material);
    mesh.scale.set(0.25, 0.25, 0.25); 
    scene.add(mesh);
    
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById("background").appendChild(renderer.domElement);

    window.addEventListener('resize', onWindowResize, false);
}

function animate() {
    requestAnimationFrame(animate);
    mesh.rotation.y += 0.001;  // ここで全天球画像を回転させます
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}
