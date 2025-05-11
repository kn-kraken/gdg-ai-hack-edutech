<script lang="ts">
	import Popover from './Popover.svelte';

	export let text;
	export let note: string | null = null;

	let hovered = false;
</script>

<li class="ml-4" on:mouseover={() => (hovered = true)} on:mouseleave={() => (hovered = false)}>
	{text}
</li>
{#if hovered && note}
	<Popover text={note} />
{/if}
