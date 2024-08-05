$(document).ready(function() {
	const $random = $('.nbr');
	const $timer = 30;
	let $it;
	let $data = 0;
	let index;
	let change;
	let letters = ['p', 'a', 't', 't', 'e', 'r', 'n'];
	
	$random.each(function() {
		change = Math.round(Math.random() * 100);
		$(this).attr('data-change', change);
	})
	
	function random() {
		return Math.round(Math.random() * 9);
	}
	
	function select() {
		return Math.round(Math.random() * $random.length + 1);
	}
	
	function value() {
		$('.nbr:nth-child(' + select() + ')').html('' + random() + '');
		$('.nbr:nth-child(' + select() + ')').attr('data-number', $data);
		$data++;
		
		$random.each(function() {
			if (parseInt($(this).attr('data-number')) > parseInt($(this).attr('data-change'))) {
				index = $('.ltr').index(this);
				$(this).html(letters[index]);
				$(this).removeClass('nbr');
			}
		})
	}
	
	$it = setInterval(value, $timer);
})

const randomizeLetters = (letters) => {
    return new Promise((resolve, reject) => {
        const lettersTotal = letters.length;
        let cnt = 0;

        letters.forEach((letter, pos) => { 
            let loopTimeout;
            const loop = () => {
                letter.innerHTML = chars[getRandomInt(0,charsTotal-1)];
                loopTimeout = setTimeout(loop, getRandomInt(50,500));
            };
            loop();

            const timeout = setTimeout(() => {
                clearTimeout(loopTimeout);
                letter.style.opacity = 1;
                letter.innerHTML = letter.dataset.initial;
                ++cnt;
                if ( cnt === lettersTotal ) {
                    resolve();
                }
            }, pos*lineEq(40,0,8,200,lettersTotal));
        });
    });
};

this.DOM.titleLetters = Array.from(this.DOM.texts.title.querySelectorAll('span')).sort(() => 0.5 - Math.random());
this.DOM.titleLetters.forEach(letter => letter.dataset.initial = letter.innerHTML);