<script type="text/javascript">
function validate(phone) {
//  const regex = /^\(?([0-9]{3,5})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4,5})$/;
//  const regex = /^(?([0-9]{3,5})\)?[-. ]*([0-9]{3})[-. ]*([0-9]{4,5})$/;
  const regex = /^[+\(\)\-. ,0-9]{3,}$/;
  return regex.test(phone);
}

phonenumbers = document.getElementsByTagName("a");
for (var i = 0; i < phonenumbers.length; i++) {
  if(validate(phonenumbers[i].innerHTML)){
    phonenumbers[i].addEventListener('click',fn, false);
  }
}
function fn(ev){
	ev.preventDefault();
	Android.clickCall(this.innerHTML);
}
</script>
