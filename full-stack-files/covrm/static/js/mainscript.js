$(document).ready(function () {
    $('#dashboard-table').DataTable();
    $('#dashboard-table2').DataTable();

    // To select proper region from the respective state
    var $select1 = $( '#stateSelect' ),
    $select2 = $( '#regionSelect' ),
    $options = $select2.find( 'option' );

    $select1.on( 'change', function() {
        $select2.html( $options.filter( '[class="' + this.value + '"]' ) );
    }).trigger( 'change' );
});

setTimeout(function() {
    $('#message').fadeOut('slow');
}, 3000);