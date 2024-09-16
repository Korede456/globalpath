$(document).ready(function () {
  /**
   *  ====================================
   * ALL USED VARIABLES
   * ====================================
   **/
  const BASEurl = "http://localhost:8000/jobseeker/find-jobs/";
  /**
   *  ====================================
   * FETCHING ALL JOBS DYNAMICALLY USING AJAX
   * ====================================
   **/
  const fetchJobs = (query = "") => {
    $.ajax({
      url: BASEurl, // Adjust the URL as necessary
      method: "GET",
      data: { search: query },
      success: function (response) {
        // Handle the response
        console.log(response.jobs); // Logs the list of jobs
        // You can now dynamically render these jobs in your HTML
      },
      error: function (error) {
        console.error("Error fetching jobs:", error);
      },
    });
  };

  fetchJobs();

  /**
   *  ====================================
   * GETTIG SINGLE JOB DATA
   * ====================================
   **/

  // Select the input element(s)
  var search_input = $("input[name='search']");

  // Add an event listener to the input(s)
  search_input.on("input", function () {
    console.log("iput changed to:" + $(this).val());
  });
});
