var fetchData = function(email,product){
    console.log(email,product); 
    $.ajax({
        type: 'POST',
        url: "/_show_entries",
        data: {
            candidate_email: email,
            productName:product
        },
        dataType: "text",
        success: function(data){
                    data=JSON.parse(data);
                    console.log(data);

                    var entries;
                    if(data.candidate!=null)
                        entries=data.candidate.entries;
                    else
                        entries=0;
                    $('#before-email').css('display','none');
                    $('#email').val(email);
                    $('#after-email').css('display','block');
                    $('#your-entries').html(entries);
                }
        });
    $('.change-email').on('click',function(){
        sessionStorage.removeItem("email"); 
        location.reload();
    })
    $('.your-email').html(email);
}
if(sessionStorage.getItem("email")){
    var can_email=sessionStorage.getItem("email");
    fetchData(can_email,productName);
}
else{
    $('#find_email').on('click',function(){
        var can_email=$('#candidate_email').val();
        if(validateEmail(can_email)){
            fetchData(can_email,productName);   
            sessionStorage.setItem("email",can_email);   
        }
        else alert("Please enter a valid email")
    })
    document.getElementById('candidate_email').onkeydown = function(e){
        if(e.keyCode == 13){
          $('#find_email').click();
        }
     };
}