<script lang="ts">
    const files: string[] = [
      "Audionyx Prompt",
      "Implement Copy all in EWgent",
      "Implement NiceGUI and other frameworks in Pyder",
    ];

    function openFile(file: string) {
      console.log(`Open: ${file}`)
    }

    function deleteFile(file: string) {
      console.log(`Delete: ${file}`)
    }

    function createFile() {
      console.log("create file")
    }
</script>

<main>
    {#each files as file}
        <div class="filesButton">
            <button class="open" onclick={() => openFile(file)}><span>{file}</span></button>
            <button class="delete" onclick={() => deleteFile(file)}><b>x</b></button>
        </div>
    {/each}
    <button onclick={() => createFile()} style="text-align: center;"><b>+</b></button>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        resize: horizontal;
        min-width: 200px;
        max-width: 400px;
        padding: 10px;
        gap: 5px;

        button {
            border: none;
            color: var(--text);
            background-color: var(--card);
            padding: 10px 15px;
            transition: all 0.1s ease-out;
            border-radius: 5px;
            text-align: left;

            &:hover {
                filter: brightness(120%)
            }
        }

        .filesButton {
            display: flex;
            min-width: 200px;
            max-width: 400px;
            gap: 5px;

            .open {
                flex: 1;
            }

            .delete:hover {
                background-color: var(--exit);
            }
        }
    }
</style>