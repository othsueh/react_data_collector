<script lang="ts">
	type Variant = 'label' | 'create' | 'start' | 'end' | 'custom';
	type BtnType = 'button' | 'submit' | 'reset';

	const {
		variant = 'create',
		type = 'button',
		onclick,
		customBg = '',
		customHover = '',
		className = '',
		formaction,            // add
		disabled               // optional pass-through
	} = $props<{
		variant?: Variant;
		type?: BtnType;
		onclick?: (e: MouseEvent) => void;
		customBg?: string;
		customHover?: string;
		className?: string;
		formaction?: string;   // add
		disabled?: boolean;    // optional
	}>();

	const base =
		'w-48 text-white text-t3 italic font-bold py-2.5 px-6 rounded-full transition-colors duration-200 shadow-md';

	const variantBg: Record<string, string> = {
		label: 'bg-label hover:bg-teal-800',
		create: 'bg-create hover:bg-blue-600',
		start: 'bg-start hover:bg-green-600',
		end: 'bg-end hover:bg-pink-600',
		custom: `${customBg} ${customHover}`.trim()
	};

	const colors = variantBg[variant] ?? variantBg.create;
</script>

<button type={type} class={`${base} ${colors} ${className}`} onclick={onclick} {formaction} {disabled}>
	<slot />
</button>