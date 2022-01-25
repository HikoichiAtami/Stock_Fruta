function get_fruit_id(){
    fruit_id = $('select[name=fruit] option').filter(':selected').val()
    fetch("/search_stock", {
        method: "POST",
        body: JSON.stringify({ fruit_id: fruit_id }),
      });
}


