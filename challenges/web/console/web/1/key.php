<?php
$password = '639969e90d236a736ebc83fad8aa36d7';
if(array_key_exists('HTTP_REFERER', $_SERVER)&&preg_match('/(\/%23console.html)+/', $_SERVER['HTTP_REFERER'])){
    echo('Password: '.$password);
}else{
    echo("It's not that easy, but nice try. <br/><b> Go back and try again</b>");
}
?>