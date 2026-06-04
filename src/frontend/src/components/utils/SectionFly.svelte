<script lang="ts">
    import { fly } from 'svelte/transition';
    import { cubicOut } from 'svelte/easing';

    let { children, yIn = 20, yOut = -20, durationIn = 400, durationOut = 300 } = $props();
</script>

<div 
    class="sectionFly"
    in:fly={{ y: yIn, duration: durationIn, easing: cubicOut, opacity: 0 }}
    out:fly={{ y: yOut, duration: durationOut, opacity: 0 }}
>
    {@render children?.()}
</div>

<style>
    .sectionFly {
        /* Ensure the wrapper doesn't break parent layout */
        display: contents; 
    }
</style>
