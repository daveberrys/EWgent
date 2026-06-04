<script lang="ts">
    import { onMount } from "svelte";
    import { getPyAPI } from "../utils/pywebview";
    import Modal from "./utils/Modal.svelte";

    let { onSelect, onDelete }: { onSelect?: (name: string) => void, onDelete?: (name: string) => void } = $props();

    let pyAPI: any = $state(null);
    let files: string[] = $state([]);
    let selectedFile: string | null = $state(null);
    let searchQuery: string = $state("");
    
    let sidebarWidth: number = $state(260);
    let isResizing: boolean = $state(false);

    let showCreateModal = $state(false);
    let showRenameModal = $state(false);
    let showDeleteModal = $state(false);
    let newFileName = $state("");
    let renameOldName = $state("");
    let renameNewName = $state("");
    let deleteTarget = $state("");

    let filteredFiles = $derived(
        files.filter(f => f.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    onMount(async () => {
        pyAPI = await getPyAPI();
        files = await pyAPI.getFiles();
        
        const savedWidth = localStorage.getItem('sidebarWidth');
        if (savedWidth) sidebarWidth = parseInt(savedWidth);
    });

    function startResizing() {
        isResizing = true;
        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', stopResizing);
    }

    function handleMouseMove(e: MouseEvent) {
        if (!isResizing) return;
        const newWidth = e.clientX;
        if (newWidth > 150 && newWidth < 600) {
            sidebarWidth = newWidth;
        }
    }

    function stopResizing() {
        isResizing = false;
        localStorage.setItem('sidebarWidth', sidebarWidth.toString());
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', stopResizing);
    }

    async function selectFile(file: string) {
        selectedFile = file;
        onSelect?.(file);
    }

    function openCreateModal() {
        newFileName = "";
        showCreateModal = true;
    }

    async function handleCreateConfirm() {
        if (newFileName && newFileName.trim()) {
            const fileName = newFileName.trim();
            await pyAPI.saveFile(fileName, "");
            files = await pyAPI.getFiles();
            selectFile(fileName);
            showCreateModal = false;
        }
    }

    function openRenameModal(file: string, event: MouseEvent) {
        event.stopPropagation();
        renameOldName = file;
        renameNewName = file;
        showRenameModal = true;
    }

    async function handleRenameConfirm() {
        if (renameNewName && renameNewName.trim() && renameNewName !== renameOldName) {
            const success = await pyAPI.renameFile(renameOldName, renameNewName.trim());
            if (success) {
                files = await pyAPI.getFiles();
                if (selectedFile === renameOldName) {
                    selectedFile = renameNewName.trim();
                    onSelect?.(selectedFile);
                }
                showRenameModal = false;
            }
        }
    }

    function openDeleteModal(file: string, event: MouseEvent) {
        event.stopPropagation();
        deleteTarget = file;
        showDeleteModal = true;
    }

    async function handleDeleteConfirm() {
        if (deleteTarget) {
            if (selectedFile === deleteTarget) {
                selectedFile = null;
            }
            onDelete?.(deleteTarget);
            await pyAPI.deleteFile(deleteTarget);
            files = await pyAPI.getFiles();
            showDeleteModal = false;
        }
    }
</script>

<aside style="width: {sidebarWidth}px">
    <div class="sidebarHeader">
        <span class="title">EXPLORER</span>
        <button class="addBtn" onclick={openCreateModal} title="New File">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        </button>
    </div>

    <div class="searchContainer">
        <div class="searchInputWrapper">
            <svg class="searchIcon" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input 
                type="text" 
                placeholder="Search files..." 
                bind:value={searchQuery}
                spellcheck="false"
            />
        </div>
    </div>
    
    <div class="fileList">
        {#each filteredFiles as file}
            <div 
                class="fileItem" 
                class:active={selectedFile === file}
                onclick={() => selectFile(file)}
                role="button"
                tabindex="0"
                onkeydown={(e) => e.key === 'Enter' && selectFile(file)}
            >
                <svg class="fileIcon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>
                <span class="fileName">{file}</span>
                <div class="itemActions">
                    <button class="editBtn" onclick={(e) => openRenameModal(file, e)} title="Rename">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    </button>
                    <button class="deleteBtn" onclick={(e) => openDeleteModal(file, e)} title="Delete">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                </div>
            </div>
        {/each}
        
        {#if filteredFiles.length === 0}
            <div class="emptyState">
                {searchQuery ? 'No matches found' : 'No files yet'}
            </div>
        {/if}
    </div>
    
    <div class="resizer" onmousedown={startResizing}></div>
</aside>

<!-- Modal Popups -->
<Modal 
    show={showCreateModal} 
    title="Create New File" 
    onClose={() => showCreateModal = false} 
    onConfirm={handleCreateConfirm}
    confirmText="Create"
>
    <div class="inputField">
        <label for="newFile">File Name</label>
        <input id="newFile" type="text" bind:value={newFileName} placeholder="Enter name..." autofocus />
    </div>
</Modal>

<Modal 
    show={showRenameModal} 
    title="Rename File" 
    onClose={() => showRenameModal = false} 
    onConfirm={handleRenameConfirm}
    confirmText="Rename"
>
    <div class="inputField">
        <label for="renameFile">New Name</label>
        <input id="renameFile" type="text" bind:value={renameNewName} placeholder="Enter new name..." autofocus />
    </div>
</Modal>

<Modal 
    show={showDeleteModal} 
    title="Delete File" 
    onClose={() => showDeleteModal = false} 
    onConfirm={handleDeleteConfirm}
    confirmText="Delete"
    confirmColor="var(--danger)"
>
    <p>Are you sure you want to permanently delete <strong>{deleteTarget}</strong>?</p>
    <p class="warning">This action cannot be undone.</p>
</Modal>
<!-- End of modal popups -->

<style>
    aside {
        background-color: var(--bg-tertiary);
        border-right: 1px solid var(--border-primary);
        display: flex;
        flex-direction: column;
        user-select: none;
        position: relative;
        min-width: 150px;

        .resizer {
            position: absolute;
            right: -3px;
            top: 0;
            bottom: 0;
            width: 6px;
            cursor: col-resize;
            z-index: 10;
            transition: background-color 0.2s;
            &:hover { background-color: var(--accent-primary); }
        }

        .sidebarHeader {
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;

            .title {
                font-size: 11px;
                font-weight: 700;
                color: var(--text-secondary);
                letter-spacing: 0.1em;
            }

            .addBtn {
                color: var(--text-secondary);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 4px;
                border-radius: 4px;

                &:hover {
                    background-color: var(--hover-overlay);
                    color: var(--text-primary);
                }
            }
        }

        .searchContainer {
            padding: 0 12px 8px 12px;

            .searchInputWrapper {
                display: flex;
                align-items: center;
                background-color: var(--bg-primary);
                border: 1px solid var(--border-primary);
                border-radius: 4px;
                padding: 0 8px;
                gap: 8px;

                .searchIcon {
                    color: var(--text-muted);
                }

                input {
                    flex: 1;
                    background: none;
                    border: none;
                    outline: none;
                    color: var(--text-primary);
                    padding: 6px 0;
                    font-size: 12px;

                    &::placeholder {
                        color: var(--text-muted);
                    }
                }
            }
        }

        .fileList {
            flex: 1;
            overflow-y: auto;
            padding: 8px 0;

            .fileItem {
                display: flex;
                align-items: center;
                padding: 8px 16px;
                cursor: pointer;
                gap: 10px;
                position: relative;
                transition: background-color 0.1s;

                &:hover {
                    background-color: var(--hover-overlay);
                }

                &.active {
                    background-color: var(--active-overlay);
                    color: var(--accent-primary);

                    &::before {
                        content: '';
                        position: absolute;
                        left: 0;
                        top: 0;
                        bottom: 0;
                        width: 2px;
                        background-color: var(--accent-primary);
                    }
                    .fileIcon { color: var(--accent-primary); }
                }

                .fileIcon {
                    color: var(--text-secondary);
                    flex-shrink: 0;
                }

                .fileName {
                    font-size: 13px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    flex: 1;
                }

                .itemActions {
                    display: flex;
                    gap: 4px;

                    .editBtn, .deleteBtn {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 24px;
                        height: 24px;
                        border-radius: 4px;
                        transition: all 0.2s ease;
                        flex-shrink: 0;
                        color: var(--text-secondary);
                        
                        &:hover { color: white; }
                    }

                    .editBtn:hover { background-color: var(--accent-primary); }
                    .deleteBtn:hover { background-color: var(--danger); }
                }
            }
        }
    }

    .inputField {
        display: flex;
        flex-direction: column;
        gap: 8px;

        label {
            font-size: 12px;
            color: var(--text-secondary);
        }

        input {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            padding: 8px 12px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
            &:focus { border-color: var(--accent-primary); }
        }
    }

    .warning {
        color: var(--danger);
        font-size: 12px;
        margin-top: 8px;
        opacity: 0.8;
    }
</style>
