import Split from 'split.js';

/**
 * Returns a Split object with 3 rows (for the main page with "My models" / Treeview / "Impact by task")
 *
 * @param document 	the html Document() object
 * @returns 		Split object
 */
export function get3RowsSplitObject(document: Document) {
	return Split(['#split-0', '#split-1', '#split-2'], {
		sizes: [25, 50, 25],
		minSize: 0,
		snapOffset: 150,
		onDrag: function () {
			for (let i = 0; i < 3; i++) {
				let element = document.getElementById('split-' + i);
				if (element!.offsetWidth === 0) {
					element!.style.visibility = 'hidden';
				} else {
					element!.style.visibility = 'visible';
				}
			}
		}
	});
}

/**
 * Returns a Split object with 2 rows (for the compare page with "My models" / "Differences")
 *
 * @param document 	the html Document() object
 * @returns 		Split object
 */
export function get2RowsSplitObject(document: Document) {
	return Split(['#split-0', '#split-1'], {
		sizes: [25, 75],
		minSize: 0,
		snapOffset: 150,
		onDrag: function () {
			for (let i = 0; i < 2; i++) {
				let element = document.getElementById('split-' + i);
				if (element!.offsetWidth === 0) {
					element!.style.visibility = 'hidden';
				} else {
					element!.style.visibility = 'visible';
				}
			}
		}
	});
}
