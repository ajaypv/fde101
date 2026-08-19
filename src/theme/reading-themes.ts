export const READING_THEME_STORAGE_KEY = 'fde101-reading-theme';

export const READING_THEMES = [
	{
		value: 'minimal',
		label: 'Minimal',
		description: 'The clean black-and-white reading style.',
	},
	{
		value: 'newspaper',
		label: 'Newspaper',
		description: 'Warm paper, serif headlines, and editorial rules.',
	},
	{
		value: 'gazette',
		label: 'Gazette',
		description: 'Blue-black ink, paper grain, and a magazine-style editorial grid.',
	},
] as const;

export type ReadingTheme = (typeof READING_THEMES)[number]['value'];

export const DEFAULT_READING_THEME: ReadingTheme = 'minimal';

export function parseReadingTheme(value: unknown): ReadingTheme {
	return READING_THEMES.some((theme) => theme.value === value)
		? (value as ReadingTheme)
		: DEFAULT_READING_THEME;
}
