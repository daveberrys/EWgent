<script lang="ts">
    import { onMount } from "svelte";
    import { getPyAPI } from "../utils/pywebview";

    let { fileName }: { fileName: string | null } = $props();

    let pyAPI: any = $state(null);
    let content: string = $state("");
    let saveTimer: ReturnType<typeof setTimeout> | null = $state(null);

    onMount(async () => {
        pyAPI = await getPyAPI();
    });

    async function loadContent(name: string) {
        content = await pyAPI.getFileContent(name);
    }

    function scheduleSave() {
        if (saveTimer) clearTimeout(saveTimer);
        saveTimer = setTimeout(async () => {
            if (fileName) {
                await pyAPI.saveFile(fileName, content);
            }
        }, 100);
    }

    $effect(() => {
        if (fileName && pyAPI) {
            loadContent(fileName);
        } else if (!fileName) {
            content = "";
        }
    });
</script>

<main>
    {#if fileName}
        <div class="editor">
            <section class="topbar">
                <span class="fileName">{fileName}</span>
                <button onclick={async () => { pyAPI.copyToClipboard(content); }} class="copy">Copy</button>
            </section>
            <textarea bind:value={content} oninput={scheduleSave} placeholder="Type something here!"></textarea>
        </div>
    {:else}
        <div class="empty">
            <p>Select a file to start editing</p>
        </div>
    {/if}
</main>

<style>
    main {
        display: flex;
        flex: 1;
        min-height: 0;

        .editor {
            display: flex;
            flex-direction: column;
            flex: 1;
            min-height: 0;
            margin-top: 10px;

            .topbar {
                display: flex;
                align-items: center;

                .fileName {
                    color: var(--file);
                    font-size: 0.85rem;
                }

                .copy {
                    margin-left: auto;
                    background-color: var(--button);
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    cursor: pointer;
                    font-size: 0.85rem;
                }
            }

            textarea {
                background-color: var(--background);
                color: white;
                flex: 1;
                border: none;
                outline: none;
                resize: none;
                padding: 10px 15px;
                font-family: inherit;
                font-size: inherit;
            }
        }
        
        .empty {
            display: flex;
            flex: 1;
            align-items: center;
            justify-content: center;
            color: #888;
        }
    }
</style>
