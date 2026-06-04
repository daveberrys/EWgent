<script lang="ts">
    import { onMount } from "svelte";
    import SectionFly from "./utils/SectionFly.svelte";
    import { getPyAPI } from "../utils/pywebview";

    let { fileName }: { fileName: string | null } = $props();

    let pyAPI: any = $state(null);
    let content: string = $state("");
    let saveTimer: ReturnType<typeof setTimeout> | null = $state(null);
    let isSaving: boolean = $state(false);

    let lineCount = $derived(content.split('\n').length);
    let wordCount = $derived(content.trim() ? content.trim().split(/\s+/).length : 0);
    let charCount = $derived(content.length);
    
    let tokenEstimate = $derived(Math.ceil(charCount / 3.8));

    onMount(async () => {
        pyAPI = await getPyAPI();
    });

    async function loadContent(name: string) {
        content = await pyAPI.getFileContent(name);
    }

    function scheduleSave() {
        isSaving = true;
        if (saveTimer) clearTimeout(saveTimer);
        saveTimer = setTimeout(async () => {
            if (fileName) {
                await pyAPI.saveFile(fileName, content);
                isSaving = false;
            }
        }, 500);
    }

    async function copyContent() {
        if (pyAPI && content) {
            const success = await pyAPI.copyToClipboard(content);
            if (success) {
                console.log("Copied to clipboard");
            }
        }
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
    {#if !fileName}
        <SectionFly yIn={20} yOut={-20}>
            <div class="emptyState">
                <div class="hero">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="emptyIcon"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                    <h1>Welcome to Pyder</h1>
                    <p>A modern documentation workspace for developers.</p>
                </div>
                <div class="gettingStarted">
                    <p>Select a file from the explorer or create a new one to begin writing.</p>
                </div>
            </div>
        </SectionFly>
    {:else}
        <SectionFly yIn={20} yOut={-20}>
            <div class="editorContainer">
                <header class="editorHeader">
                    <div class="breadcrumb">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="breadcrumbIcon"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>
                        <div class="breadcrumbContent">
                            {#key fileName}
                                <SectionFly yIn={10} yOut={-10} durationIn={300} durationOut={200}>
                                    <span class="breadcrumbItem">{fileName}</span>
                                </SectionFly>
                            {/key}
                        </div>
                    </div>
                    
                    <div class="actions">
                        {#if isSaving}
                            <span class="statusIndicator">Saving...</span>
                        {:else}
                            <span class="statusIndicator">All changes saved</span>
                        {/if}
                        <button class="actionBtn" onclick={copyContent} title="Copy to clipboard">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                            <span>Copy</span>
                        </button>
                    </div>
                </header>
                
                <div class="textareaWrapper">
                    {#key fileName}
                        <SectionFly yIn={20} yOut={-20}>
                            <textarea 
                                bind:value={content} 
                                oninput={scheduleSave} 
                                placeholder="Start typing your documentation..."
                                spellcheck="false"
                            ></textarea>
                        </SectionFly>
                    {/key}
                </div>

                <footer class="editorFooter">
                    <div class="stats">
                        {#key fileName}
                            <SectionFly yIn={10} yOut={-10} durationIn={300} durationOut={200}>
                                <div class="statsContent">
                                    <div class="statItem" title="Estimated AI Tokens (based on ~4 chars/token)">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                                        <span>~{tokenEstimate} tokens</span>
                                    </div>
                                    <span class="separator">|</span>
                                    <span>{lineCount} lines</span>
                                    <span class="separator">|</span>
                                    <span>{wordCount} words</span>
                                    <span class="separator">|</span>
                                    <span>{charCount} characters</span>
                                </div>
                            </SectionFly>
                        {/key}
                    </div>
                    <div class="encoding">
                        <span>UTF-8</span>
                    </div>
                </footer>
            </div>
        </SectionFly>
    {/if}
</main>

<style>
    main {
        display: flex;
        flex: 1;
        min-height: 0;
        background-color: var(--bg-primary);
        position: relative;

        :global(.sectionFly) {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
        }

        .emptyState, .editorContainer {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .editorContainer {
            .editorHeader {
                height: 36px;
                padding: 0 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: var(--bg-secondary);
                border-bottom: 1px solid var(--border-primary);

                .breadcrumb {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    color: var(--text-secondary);
                    font-size: 12px;

                    .breadcrumbContent {
                        display: grid;
                        grid-template-columns: 1fr;
                        align-items: center;

                        :global(.sectionFly) {
                            position: relative;
                            grid-area: 1 / 1;
                        }

                        .breadcrumbItem {
                            white-space: nowrap;
                        }
                    }

                    .breadcrumbIcon {
                        color: var(--accent-primary);
                    }
                }

                .actions {
                    display: flex;
                    align-items: center;
                    gap: 16px;

                    .statusIndicator {
                        font-size: 11px;
                        color: var(--text-muted);
                    }

                    .actionBtn {
                        display: flex;
                        align-items: center;
                        gap: 6px;
                        padding: 2px 8px;
                        border-radius: 4px;
                        font-size: 11px;
                        color: var(--text-secondary);

                        &:hover {
                            background-color: var(--hover-overlay);
                            color: var(--text-primary);
                        }
                    }
                }
            }

            .textareaWrapper {
                flex: 1;
                display: grid;
                grid-template-columns: 1fr;
                min-height: 0;
                position: relative;
                overflow: hidden;

                :global(.sectionFly) {
                    position: relative;
                    grid-area: 1 / 1;
                    display: flex;
                }

                textarea {
                    flex: 1;
                    background-color: transparent;
                    color: var(--text-primary);
                    border: none;
                    outline: none;
                    resize: none;
                    padding: 24px;
                    font-family: var(--font-mono);
                    font-size: 15px;
                    line-height: 1.6;
                    overflow-y: auto;
                }
            }

            .editorFooter {
                height: 24px;
                background-color: var(--accent-secondary);
                color: white;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 16px;
                font-size: 11px;

                .stats {
                    display: grid;
                    grid-template-columns: 1fr;
                    align-items: center;

                    :global(.sectionFly) {
                        position: relative;
                        grid-area: 1 / 1;
                    }

                    .statsContent {
                        display: flex;
                        align-items: center;
                        gap: 12px;

                        .statItem {
                            display: flex;
                            align-items: center;
                            gap: 6px;
                            color: white;
                        }

                        .separator {
                            opacity: 0.3;
                            font-weight: 100;
                        }
                    }
                }
            }
        }

        .emptyState {
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            text-align: center;
            padding: 40px;
            background-color: var(--bg-primary);

            .hero {
                margin-bottom: 32px;

                .emptyIcon {
                    margin-bottom: 24px;
                    color: var(--accent-primary);
                }

                h1 {
                    color: var(--text-primary);
                    font-size: 28px;
                    margin-bottom: 12px;
                    font-weight: 700;
                }
            }

            .gettingStarted {
                border-top: 1px solid var(--border-primary);
                padding-top: 32px;
                max-width: 400px;

                p {
                    font-size: 14px;
                }
            }
        }
    }
</style>
