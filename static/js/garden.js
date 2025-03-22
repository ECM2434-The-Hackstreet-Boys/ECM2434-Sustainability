//Author: Edward Pratt


//Function: Creates a PIXI.js application for the garden, and creates a base isometric grid when the page is loaded.
// The grid is created using a for loop to create a 10x10 grid of isometric tiles. The tiles are created using the PIXI.Sprite class
// and are added to a PIXI.Container. The tiles are then rendered in the correct order to ensure the correct depth sorting.
// The grid is then displayed on the screen by appending the PIXI canvas to the game container element.
// When the page is loaded a call is made to django to retrieve the garden state which is then loaded onto the created canvas.
document.addEventListener("DOMContentLoaded", async function () {
    console.log("Script loaded and DOM fully parsed!");

    // Retrieves the game container element and the game wrapper element from the HTML document
    const gameContainer = document.getElementById('game-container');
    const gameWrapper = document.getElementById('game-wrapper');


    // If the game container element is not found, an error message is displayed in the console and the function is returned
    if (!gameContainer) {
        console.error("The game container element was not found!");
        return;
    }


    // Creates a new PIXI application and initializes it with the specified width, height and background color
    const app = new PIXI.Application();
    await app.init({
        width: 800,
        height: 800,
        backgroundColor: 0x1099bb,
    });

    // Appends the PIXI canvas to the game container element
    console.log("Pixi app initialized and canvas appended!");
    gameContainer.appendChild(app.canvas);


    // Creates a gridContainer for storing the isometric tiles
    const gridContainer = new PIXI.Container();
    app.stage.addChild(gridContainer);
    //
    // // Load the isometric textures for the blocks
    // console.log("Loading isometric texture...");
    // const grasstexture = await PIXI.Assets.load('../static/resources/tileGrass.png?v=${Date.now()}');
    // const treetexture = await PIXI.Assets.load('../static/resources/tileTree.png?v=${Date.now()}');
    // const flowertexture = await PIXI.Assets.load('../static/resources/tileFlower.png?v=${Date.now()}');
    // const flowerPinkTexture = await PIXI.Assets.load('../static/resources/tileFlowerPink.png?v=${Date.now()}');
    //
    //
    // // Store the textures in an object for easy access
    // const textures = {
    //     grass: grasstexture,
    //     tree: treetexture,
    //     flower: flowertexture,
    //     flowerPink: flowerPinkTexture,
    // };
    //
    // console.log("Texture loaded:", grasstexture);
    const textures = {};
    async function loadAssets() {
        const response = await fetch('/api/assets/');
        const data = await response.json();
        console.log("API RESPONSE:", data);


        for(const asset of data.assets){
            if (!asset.blockPath) {
                console.error(`Missing file path for asset: ${asset.name}`);
                continue;
            }

            const assetPath = `../${asset.blockPath}?v=${Date.now()}`;
            console.log(`Loading: ${assetPath}`);
            textures[asset.name] = await PIXI.Assets.load(assetPath);


        }
        return textures;
    }

    await loadAssets()

    // Tile configuration
    const TILE_WIDTH = 64;
    const TILE_HEIGHT = 32;
    const TILE_DEPTH = 32;
    const mapWidth = 10;
    const mapHeight = 10;
    const SPACING = 0;


    // Initialises the tileData object which will store the tile data for each tile
    let tileData = {};


    // Loop through rows and columns to create the isometric grid
    for (let isoY = 0; isoY < mapHeight; isoY++) {
        for (let isoX = 0; isoX < mapWidth; isoX++) {
            const isoZ = 0; // Fixed height (1)

            // Calculate the screen position based on the isometric coordinates
            const screenX = (isoX - isoY) * (TILE_WIDTH / 2) + SPACING;
            const screenY = (isoX + isoY) * (TILE_HEIGHT / 2) - (isoZ * TILE_DEPTH) + SPACING;

            // Create a new tile sprite
            let tile = new PIXI.Sprite(textures.Grass);
            tile.width = TILE_WIDTH;
            tile.height = TILE_HEIGHT + TILE_DEPTH;

            // Set the tile location to the correct place
            tile.anchor.set(0.5, 1);
            tile.x = screenX + 400; // Add offset for better positioning on screen
            tile.y = screenY + 100; // Add offset for better positioning on screen
            tile.zIndex = isoZ; // Store the z-index for depth sorting

            // Enable interactivity
            tile.interactive = true;
            tile.buttonMode = true; // Enable clickable functionality

            // Store the isometric coordinates for later use
            tile.isoX = isoX;
            tile.isoY = isoY;

            // Store the tile data for later reference
            tileData[`${isoX},${isoY}`] = {type: 'block', sprite: tile, textureType: 'Grass'};

            // Add the tile to the grid container
            gridContainer.addChild(tile);
        }
    }

    // Ensure the tiles are rendered in the correct order (depth sorting)
    app.ticker.add(() => {
        gridContainer.children.sort((a, b) => a.y - b.y);
    });

    // Loads the garden on page load
    await loadGarden();


    // Function to save the garden state to the database
    async function saveGarden() {
        const gardenState = getTileState();
        const response = await fetch('save_garden/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({garden: gardenState}),
        });
        if (response.ok) {
            console.log('Garden saved successfully');
        } else {
            console.error('Failed to save garden');
        }
    }


    // Function to load the garden state from the database
    async function loadGarden() {
        const response = await fetch('load_garden/');
        if (response.ok) {
            const data = await response.json();
            loadTileState(data.garden);
            console.log('Garden loaded successfully');
        } else {
            console.error('Failed to load garden');
        }
    }

    async function placeBlock(tile, blockName){
        let response = await fetch('/api/place_block/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },

            body: JSON.stringify({blockName: blockName, currentTile: tileData[`${tile.isoX},${tile.isoY}`].textureType}),
        });
        let data = await response.json();
        if (data.success){
            console.log("Block Placed Successfully")
        } else {
            alert(data.message);
        }
        return data;

    }

    async function removeBlock(tile, blockID) {
        let response = await fetch("/api/remove_block/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ block_id: blockID })
        });

        let data = await response.json();
        if (data.success) {
            console.log("Block removed and added to inventory!");
        } else {
            alert(data.message);
        }
    }

    // Function to retrieve the CSRF token from the page
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }


    // Event listeners for the save and load garden buttons
    document.getElementById('save-button').addEventListener('click', saveGarden);
    document.getElementById('load-button').addEventListener('click', loadGarden);


    console.log("Tiles created and added to grid container.");
    console.log("Tile Data:", tileData);


    // Function to get the current state of the tiles useful for saving the garden state
    function getTileState() {
        let state = {};
        for (let key in tileData) {
            state[key] = tileData[key].textureType;
        }
        console.log('State:', state);
        return state;
    }


    // Function to load the tile state from the database
    function loadTileState(savedState) {
        console.log('Loading Tile State', savedState);
        for (let key in savedState) {
            let textureType = savedState[key];
            let [isoX, isoY] = key.split(',').map(Number);
            console.log("Loading tile:", isoX, isoY, textureType);
            if (tileData[key]){
                tileData[key].textureType = textureType;
                tileData[key].sprite.texture = textures[textureType];


                let tileSprite = gridContainer.children.find(sprite => sprite.isoX === isoX && sprite.isoY === isoY);
                console.log("Tile Sprite:", tileSprite);
                if (tileSprite) {
                    tileSprite.texture = textures[textureType]; // Apply the correct texture
                    console.log(`Updated tile (${isoX}, ${isoY}) to texture: ${textureType}`);
                } else {
                    console.warn(`No sprite found for (${isoX}, ${isoY}) in gridContainer`);
                }
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

    // ** Context Menu **
    let contextMenu = document.getElementById('context-menu');
    let selectedTile = null;

    document.addEventListener("contextmenu", (event) => event.preventDefault()); // Disable default menu


    // Right-click event listeners for each tile
    gridContainer.children.forEach(tile => {
        tile.interactive = true;

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

        tile.on("pointerover", () => {
            tile.tint = 0xAAAAAA;
        });

        tile.on("pointerout", () => {
            tile.tint = 0xFFFFFF;
        });

    });


    // Function to show the context menu when tile pressed
    function showContextMenu(x, y, tile) {
        selectedTile = tile;
        //tile.tint = 0x999999; // Change color to indicate long press
        contextMenu.style.display = 'block';
        contextMenu.style.left = x + 'px';
        contextMenu.style.top = y + 'px';
    }


    // Hide context menu when clicking outside
    document.addEventListener("click", (event) => {
        if (!contextMenu.contains(event.target) && !document.getElementById("texture-submenu").contains(event.target)) {
            contextMenu.style.display = "none";
            selectedTile.tint = 0xFFFFFF; // Back to normal
            document.getElementById("texture-submenu").style.display = "none";
        }
    });


    // Event listener for the edit tile button
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
    submenu.innerHTML = ""; // Clear any existing buttons

    for (let key in textures) {
        const button = document.createElement("button");
        button.textContent = key;

        button.addEventListener("click", async () => {
            if (selectedTile) {
                let isoX = selectedTile.isoX;
                let isoY = selectedTile.isoY;

                // Send request to place block, check if user has inventory
                placeBlock(selectedTile, key).then(response => {
                    console.log(response);
                    if (response.success) {
                        selectedTile.texture = textures[key]; // Update texture on frontend
                        tileData[`${isoX},${isoY}`].textureType = key;
                        submenu.style.display = "none";
                    } else {
                        alert(response.message); // Show error if block cannot be placed
                    }
                });
            }
        });

        submenu.appendChild(button);
    }



});
