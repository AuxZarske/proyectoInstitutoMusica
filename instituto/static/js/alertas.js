$(document).ready(function(){
    $('#elBotonBorra').click(function(){

        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
              confirmButton: 'btn btn-success',
              cancelButton: 'btn btn-danger'
            },
            buttonsStyling: true
          })
          
          swalWithBootstrapButtons.fire({
            title: 'Estas Seguro?',
            text: "Esto no podra ser revertido!",
            type: 'Atencion',
            showCancelButton: true,
            confirmButtonText: 'Si, Borrarlo!',
            cancelButtonText: 'No, cancelar!',
            reverseButtons: true
          }).then((result) => {
            if (result.value) {
              swalWithBootstrapButtons.fire(
                'Borrado!',
                'Tu archivo fue borrado.',
                'exito'
              )
            } else if (
              /* Read more about handling dismissals below */
              result.dismiss === Swal.DismissReason.cancel
            ) {
              swalWithBootstrapButtons.fire(
                'Cancelado',
                'Tu archivo esta intacto :)',
                'error'
              )
            }
          })


    })
});

