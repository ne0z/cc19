<?php
$ok = array_key_exists("Red_Guy's_name", $_COOKIE)&&preg_match('/([Ee])(lmo)+/', $_COOKIE["Red_Guy's_name"]);

if (!$ok)
	setcookie("Red_Guy's_name", 'Name', time()+300);
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Cookie_monster</title>
    </head>
    <body>
<?php

if($ok) {
  echo('<p>flag{YummyC00k13s}</p>');
} else {
    echo("<p>He's my favorite red guy</p>");
}

?>
</body>
</html>
