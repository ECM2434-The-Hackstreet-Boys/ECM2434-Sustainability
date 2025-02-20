document.addEventListener("DOMContentLoaded", async function () {
    console.log("Script loaded and DOM fully parsed!");

    const gameContainer = document.getElementById('game-container');
    const gameWrapper = document.getElementById('game-wrapper');

    if (!gameContainer) {
        console.error("The game container element was not found!");
        return;
    }

    const app = new PIXI.Application();
    await app.init({
        width: 800,
        height: 800,
        backgroundColor: 0x1099bb,
    });

    console.log("Pixi app initialized and canvas appended!");
    gameContainer.appendChild(app.canvas);

    const gridContainer = new PIXI.Container();
    app.stage.addChild(gridContainer);

    // Load the isometric texture without using PIXI.Loader
    console.log("Loading isometric texture...");
    const grasstexture = await PIXI.Assets.load('../static/resources/grass.png?v=${Date.now()}');
    const treetexture = await PIXI.Assets.load('../static/resources/grassWithTree.png?v=${Date.now()}');

    // Store the textures in an object for easy access
    const textures = {
        block: grasstexture,
        tree: treetexture,
    };

    console.log("Texture loaded:", grasstexture);

    // Tile configuration
    const TILE_WIDTH = 64;
    const TILE_HEIGHT = 32;
    const TILE_DEPTH = 32;
    const mapWidth = 10;
    const mapHeight = 10;
    const SPACING = 0;

    let tileData = {};

    // Loop through rows and columns to create the isometric grid
    for (let isoY = 0; isoY < mapHeight; isoY++) {
        for (let isoX = 0; isoX < mapWidth; isoX++) {
            const isoZ = 0; // Fixed height (1)
            const screenX = (isoX - isoY) * (TILE_WIDTH / 2) + SPACING;
            const screenY = (isoX + isoY) * (TILE_HEIGHT / 2) - (isoZ * TILE_DEPTH) + SPACING;

            let tile = new PIXI.Sprite(textures.block);
            tile.width = TILE_WIDTH;
            tile.height = TILE_HEIGHT + TILE_DEPTH;

            tile.anchor.set(0.5, 1);
            tile.x = screenX + 400; // Add offset for better positioning on screen
            tile.y = screenY + 100; // Add offset for better positioning on screen
            tile.zIndex = isoZ; // Store the z-index for depth sorting

            tile.interactive = true;
            tile.buttonMode = true; // Enable clickable functionality

            // Store the tile data for later reference
            tileData[`${isoX},${isoY}`] = {type: 'block', sprite: tile};

            // Add the tile to the grid container
            gridContainer.addChild(tile);
        }
    }

    // Ensure the tiles are rendered in the correct order (depth sorting)
    app.ticker.add(() => {
        gridContainer.children.sort((a, b) => a.y - b.y);
    });

    console.log("Tiles created and added to grid container.");

    function getTileState() {
        let state = {};
        for (let key in tileData) {
            state[key] = tileData[key].type;
        }
        return state;
    }

    function loadTileState(savedState) {
        for (let key in savedState) {
            if (tileData[key]) {
                let type = savedState[key];
                tileData[key].type = type;
                tileData[key].sprite.texture = textures[type];
            }
        }
    }

    // Implement drag functionality
    let isDragging = false;
    let lastX = 0, lastY = 0;
    let wrapperWidth = gameWrapper.clientWidth;
    let wrapperHeight = gameWrapper.clientHeight;
    let containerWidth = gameContainer.clientWidth;
    let containerHeight = gameContainer.clientHeight;

    // Function to start dragging
    function startDrag(x, y) {
        isDragging = true;
        lastX = x;
        lastY = y;
        gameWrapper.style.cursor = 'grabbing'; // Change cursor when dragging starts
    }

    // Function to move the canvas
    function moveDrag(x, y) {
        if (isDragging) {
            const dx = x - lastX;
            const dy = y - lastY;

            let newLeft = gameContainer.offsetLeft + dx;
            let newTop = gameContainer.offsetTop + dy;

            // Prevent moving too far to the right or left
            newLeft = Math.min(0, Math.max(wrapperWidth - containerWidth, newLeft));

            // Prevent moving too far up or down
            newTop = Math.min(0, Math.max(wrapperHeight - containerHeight, newTop));

            // Apply the new position
            gameContainer.style.left = newLeft + 'px';
            gameContainer.style.top = newTop + 'px';

            lastX = x;
            lastY = y;
        }
    }

    // Function to stop dragging
    function stopDrag() {
        isDragging = false;
        gameWrapper.style.cursor = 'grab'; // Reset cursor when dragging stops
    }

    // ** Mouse Events **
    gameWrapper.addEventListener('mousedown', (e) => startDrag(e.pageX, e.pageY));
    gameWrapper.addEventListener('mousemove', (e) => moveDrag(e.pageX, e.pageY));
    gameWrapper.addEventListener('mouseup', stopDrag);
    gameWrapper.addEventListener('mouseleave', stopDrag);

    // ** Touch Events **
    gameWrapper.addEventListener('touchstart', (e) => {
        const touch = e.touches[0];
        startDrag(touch.pageX, touch.pageY);
    });

    gameWrapper.addEventListener('touchmove', (e) => {
        e.preventDefault(); // Prevent scrolling while dragging
        const touch = e.touches[0];
        moveDrag(touch.pageX, touch.pageY);
    });

    gameWrapper.addEventListener('touchend', stopDrag);
    gameWrapper.addEventListener('touchcancel', stopDrag);


    let contextMenu = document.getElementById('context-menu');
    let selectedTile = null;

    document.addEventListener("contextmenu", (event) => event.preventDefault()); // Disable default menu

    gridContainer.children.forEach(tile => {
        tile.on("rightdown", (event) => { // 'rightdown' detects right-click in Pixi.js
            event.stopPropagation(); // Prevents event from bubbling up
            event.preventDefault();  // Stops browser menu
            showContextMenu(event.global.x, event.global.y, tile);
        });

        // Long press (Mobile)
        tile.on("pointerdown", (event) => {
            pressTimer = setTimeout(() => {
                showContextMenu(event.global.x, event.global.y, tile);
            }, 500); // Hold for 500ms to trigger
            tile.on("pointerup", () => clearTimeout(pressTimer)); // Cancel if released early
            tile.on("pointerout", () => clearTimeout(pressTimer));
        });
    });

    function showContextMenu(x, y, tile) {
        selectedTile = tile;
        contextMenu.style.display = 'block';
        contextMenu.style.left = x + 'px';
        contextMenu.style.top = y + 'px';
    }

    document.addEventListener("click", (event) => {
        if (!contextMenu.contains(event.target) && !document.getElementById("texture-submenu").contains(event.target)) {
            contextMenu.style.display = "none";
            document.getElementById("texture-submenu").style.display = "none";
        }
    });

    document.getElementById("edit-tile").addEventListener("click", (event) => {
        event.stopPropagation(); // Prevents the click event from propagating
        if (selectedTile) {
            const submenu = document.getElementById("texture-submenu");
            submenu.style.display = "block";
            submenu.style.left = contextMenu.style.left;
            submenu.style.top = parseInt(contextMenu.style.top) + contextMenu.offsetHeight + 'px';
            submenu.style.zIndex = 1000; // Ensure it's on top of the context menu
        }
    });

    // Create submenu for texture options
    const submenu = document.getElementById("texture-submenu");
    for (let key in textures) {
        const button = document.createElement("button");
        button.textContent = key;
        button.addEventListener("click", () => {
            if (selectedTile) {
                selectedTile.texture = textures[key];
                tileData[`${selectedTile.x},${selectedTile.y}`].type = key;
                submenu.style.display = "none";
            }
        });
        submenu.appendChild(button);
    }

    document.getElementById("delete-tile").addEventListener("click", () => {
        if (selectedTile) {
            selectedTile.destroy(); // Remove tile
        }
    });
});