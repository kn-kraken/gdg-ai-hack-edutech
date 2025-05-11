<script>
	export let text = ''; // Text to display in popover

	let x = 0;
	let y = 0;
	let visible = true;

	function handleMouseMove(event) {
		x = event.clientX;
		y = event.clientY;
	}
</script>

<svelte:window on:mousemove={handleMouseMove} />

<div
	class="trigger"
	on:mouseenter={handleMouseEnter}
	on:mouseleave={handleMouseLeave}
	on:mousemove={handleMouseMove}
>
	<slot />

	{#if visible}
		<div class="popover" style="left: {x}px; top: {y}px;">
			<div class="text-sm text-neutral-500">From your notes:</div>
			<div>
				{text}
			</div>
		</div>
	{/if}
</div>

<style>
	.trigger {
		display: inline-block;
		position: relative;
	}

	.popover {
		position: fixed;
		transform: translate(10px, 10px);
		background: white;
		border: 1px solid #ddd;
		border-radius: 4px;
		padding: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		z-index: 1000;
		pointer-events: none;
	}
</style>
