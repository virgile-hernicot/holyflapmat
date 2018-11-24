Vue.component('todo-item', {
    template: '\
      <li>\
        <span>longitude: {{ long }},</span>\
        <span>lattitude: {{ lat }},</span>\
        <span>destination: {{ dest }}</span>\
        <button v-on:click="$emit(\'remove\')">Remove</button>\
      </li>\
    ',
    props: ['long', 'lat', 'dest']
});
var app = new Vue({
    el: '#todo-list-example',
    data: {
        newTodoText: '',
        newUserLong: '',
        newUserLat: '',
        newUserDest: '',
        todos: [
            {
                id: 1,
                title: 'Do the dishes',
                long: '123344',
                lat: '12455',
                dest: 'geneve'
            }
        ],
        nextTodoId: 2
    },
    methods: {
        addNewUser: function () {
            this.todos.push({
                id: this.nextTodoId++,
                long: this.newUserLong,
                lat: this.newUserLat,
                dest: this.newUserDest
            });
            this.newTodoText = '';
            this.newUserLat = '';
            this.newUserDest = '';
            this.newUserLong = '';
        },
        compute: function () {
            var arr = this.todos;
            $.ajax(
                {
                    url: "/compute",
                    type: "POST",
                    data: arr,
                    dataType: 'json',
                    async: true,
                    success: function(msg) {
                        console.log(msg);
                    }
                }
            );
        }
    }
});