<script lang="ts">
    import { fade, scale } from 'svelte/transition';
    import { cubicOut } from 'svelte/easing';

    let { 
        show = false, 
        title = "Modal", 
        onClose, 
        onConfirm, 
        confirmText = "Confirm", 
        confirmColor = "var(--accent-primary)",
        children 
    } = $props();

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape') onClose?.();
        if (event.key === 'Enter') onConfirm?.();
    }
</script>

{#if show}
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div 
        class="modalOverlay" 
        onclick={onClose} 
        onkeydown={handleKeydown}
        transition:fade={{ duration: 200 }}
    >
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div 
            class="modalContent" 
            onclick={e => e.stopPropagation()}
            in:scale={{ start: 0.85, duration: 200, easing: cubicOut }}
            out:scale={{ start: 0.85, duration: 150, opacity: 0 }}
        >
            <header class="modalHeader">
                <h2>{title}</h2>
                <button class="closeBtn" onclick={onClose} aria-label="Close Modal">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </header>
            
            <div class="modalBody">
                {@render children?.()}
            </div>
            
            <footer class="modalFooter">
                <button class="cancelBtn" onclick={onClose}>Cancel</button>
                <button class="confirmBtn" style="background-color: {confirmColor}" onclick={onConfirm}>{confirmText}</button>
            </footer>
        </div>
    </div>
{/if}

<style>
    .modalOverlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        backdrop-filter: blur(2px);
    }

    .modalContent {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-primary);
        border-radius: 8px;
        width: 400px;
        max-width: 90vw;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        display: flex;
        flex-direction: column;

        .modalHeader {
            padding: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border-primary);

            h2 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
                color: var(--text-primary);
            }

            .closeBtn {
                color: var(--text-muted);
                &:hover { color: var(--text-primary); }
            }
        }

        .modalBody {
            padding: 20px;
            color: var(--text-secondary);
            font-size: 14px;
        }

        .modalFooter {
            padding: 16px;
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            border-top: 1px solid var(--border-primary);
            background-color: var(--bg-tertiary);
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;

            button {
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: 500;
                transition: all 0.2s;
            }

            .cancelBtn {
                background-color: transparent;
                border: 1px solid var(--border-primary);
                color: var(--text-primary);
                &:hover { background-color: var(--hover-overlay); }
            }

            .confirmBtn {
                color: white;
                &:hover { filter: brightness(110%); }
                &:active { transform: scale(0.98); }
            }
        }
    }
</style>
