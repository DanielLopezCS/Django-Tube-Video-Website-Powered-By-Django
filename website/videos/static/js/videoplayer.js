
if (document.getElementById("vid1")) {
  videojs("vid1").ready(function() {

    var myPlayer = this;

    //Set initial time to 0
    var currentTime = 0;

    setInterval(function() {
      if (!myPlayer.paused()) {
        currentTime = myPlayer.currentTime();
      }
    }, 1000);

  });

  videojs("vid1", {"height":"auto",
"width":"auto"}).ready(function(){
    var myPlayer = this;    // Store the video object
    var aspectRatio = 4.5/8; // Make up an aspect ratio

    function resizeVideoJS(){
      // Get the parent element's actual width
      var width = document.getElementById(myPlayer.id()).parentElement.offsetWidth*.9;
      // Set width to fill parent element, Set height
      myPlayer.width(width).height( width * aspectRatio );
    }

    resizeVideoJS(); // Initialize the function
    window.onresize = resizeVideoJS; // Call the function on resize
  });

}
