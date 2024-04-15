var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
document.getElementsByTagName('head')[0].appendChild(script);

class Item {
    constructor(name, who, suburb, ref) {
        this.name = name;
        this.who = who;
        this.suburb = suburb;
        this.imageref = ref;
    }
}
