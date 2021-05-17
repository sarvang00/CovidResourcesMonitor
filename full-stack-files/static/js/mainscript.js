$(document).ready(function () {
    $('#dashboard-table').DataTable();
    $('#dashboard-table2').DataTable();


    var $select1 = $( '#inputGroupSelect01' ),
    $select2 = $( '#inputGroupSelect02' ),
    $options = $select2.find( 'option' );

    $select1.on( 'change', function() {
        $select2.html( $options.filter( '[class="' + this.value + '"]' ) );
    }).trigger( 'change' );
});

setTimeout(function() {
    $('#message').fadeOut('slow');
}, 3000);