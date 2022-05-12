import Split from 'split.js';

export function get3RowsSplitObject(document: any) {
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

export function get2RowsSplitObject(document: any) {
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
