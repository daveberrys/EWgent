<script lang="ts">
    import { onMount } from "svelte";
    import SectionFly from "./utils/SectionFly.svelte";
    import Modal from "./utils/Modal.svelte";
    import { getPyAPI } from "../utils/pywebview";

    let { fileName }: { fileName: string | null } = $props();

    let pyAPI: any = $state(null);
    let content: string = $state("");
    let saveTimer: ReturnType<typeof setTimeout> | null = $state(null);
    let isSaving: boolean = $state(false);

    // Modals state
    let showSkillsModal = $state(false);
    let showPermissionsModal = $state(false);
    let skillUrl = $state("");
    
    let permissions = $state({
        optional: [""],
        doNot: [""],
        do: [""]
    });

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

    function pushContent(newSection: string) {
        let parts = content.split('\n---\n');
        parts.push(newSection);
        content = parts.join('\n---\n');
        scheduleSave();
    }

    async function handleSkillsConfirm() {
        if (skillUrl) {
            const fetchedContent = await pyAPI.fetchUrl(skillUrl);
            if (fetchedContent) {
                pushContent(fetchedContent);
                showSkillsModal = false;
                skillUrl = "";
            } else {
                console.error("Failed to fetch skill content");
            }
        }
    }

    function handlePermissionsConfirm() {
        const filterEmpty = (arr: string[]) => arr.filter(i => i.trim() !== "");
        const opt = filterEmpty(permissions.optional);
        const dont = filterEmpty(permissions.doNot);
        const do_ = filterEmpty(permissions.do);

        if (opt.length === 0 && dont.length === 0 && do_.length === 0) {
            showPermissionsModal = false;
            return;
        }

        let lines = ["# What you should do:"];
        if (opt.length > 0) {
            lines.push("## OPTIONAL:");
            opt.forEach(i => lines.push(`- ${i}`));
        }
        if (dont.length > 0) {
            lines.push("## DO NOT:");
            dont.forEach(i => lines.push(`- ${i}`));
        }
        if (do_.length > 0) {
            lines.push("## DO:");
            do_.forEach(i => lines.push(`- ${i}`));
        }

        pushContent(lines.join('\n'));
        showPermissionsModal = false;
        permissions = { optional: [""], doNot: [""], do: [""] };
    }

    function addItem(type: 'optional' | 'doNot' | 'do') {
        permissions[type].push("");
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
                    <h1>Welcome to EWgent</h1>
                    <p>A better way to write your technical prompts without headaches, and accidental sending. (Or is that just me?)</p>
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

                        <button class="actionBtn" onclick={() => showSkillsModal = true} title="Add Skills">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
                            <span>Skills</span>
                        </button>

                        <button class="actionBtn" onclick={() => showPermissionsModal = true} title="Add Permissions">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                            <span>Permissions</span>
                        </button>

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

<Modal 
    show={showSkillsModal} 
    title="Import Skills" 
    onClose={() => showSkillsModal = false} 
    onConfirm={handleSkillsConfirm}
    confirmText="Import"
>
    <div class="inputField">
        <label for="skillUrl">Skill URL</label>
        <input id="skillUrl" type="text" bind:value={skillUrl} placeholder="https://..." autofocus />
    </div>
</Modal>

<Modal 
    show={showPermissionsModal} 
    title="Set Permissions" 
    onClose={() => showPermissionsModal = false} 
    onConfirm={handlePermissionsConfirm}
    confirmText="Add Permissions"
>
    <div class="permissionsList">
        <div class="permSection">
            <div class="sectionHeader">
                <label>OPTIONAL</label>
                <button class="addSmallBtn" onclick={() => addItem('optional')}>+</button>
            </div>
            {#each permissions.optional as item, i}
                <input type="text" bind:value={permissions.optional[i]} placeholder="Optional instruction..." />
            {/each}
        </div>

        <div class="permSection">
            <div class="sectionHeader">
                <label>DO NOT</label>
                <button class="addSmallBtn" onclick={() => addItem('doNot')}>+</button>
            </div>
            {#each permissions.doNot as item, i}
                <input type="text" bind:value={permissions.doNot[i]} placeholder="Do not instruction..." />
            {/each}
        </div>

        <div class="permSection">
            <div class="sectionHeader">
                <label>DO</label>
                <button class="addSmallBtn" onclick={() => addItem('do')}>+</button>
            </div>
            {#each permissions.do as item, i}
                <input type="text" bind:value={permissions.do[i]} placeholder="Do instruction..." />
            {/each}
        </div>
    </div>
</Modal>

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

    .inputField, .permSection {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 16px;

        label {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-secondary);
            letter-spacing: 0.05em;
        }

        input {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            padding: 8px 12px;
            color: var(--text-primary);
            font-size: 13px;
            outline: none;
            &:focus { border-color: var(--accent-primary); }
        }
    }

    .permissionsList {
        display: flex;
        flex-direction: column;
        gap: 16px;
        max-height: 400px;
        overflow-y: auto;
        padding-right: 8px;

        .permSection {
            margin-bottom: 0;
            
            .sectionHeader {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 4px;

                .addSmallBtn {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    background-color: var(--accent-primary);
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    
                    &:hover { filter: brightness(110%); }
                }
            }

            input {
                margin-bottom: 4px;
            }
        }
    }
</style>
