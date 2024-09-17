$(document).ready(function () {

  /**
   *  ====================================
   * RESETS
   * ====================================
   **/
   // get desktop blablabla :)
   const jobDetailsDesktop = $(".jobDetailsDesktop");


  const BaseURL = "http://localhost:8000/jobseeker";
  /**
   *  ====================================
   * FETCHING ALL JOBS DYNAMICALLY USING AJAX
   * ====================================
   **/


  const fetchJobs = (query = "") => {
    $.ajax({
      url: `${BaseURL}/find-jobs`, // Adjust the URL as necessary
      method: "GET",
      data: { search: query },
      success: function (response) {
        console.log(response.jobs); // Logs the list of jobs
        //dynamically render these jobs in your HTML
      },
      error: function (error) {
        console.error("Error fetching jobs:", error);
      },
    });
  };

  fetchJobs();

  /**
   *  ====================================
   * GETTING SINGLE JOB DATA
   * ====================================
   **/

    jobDetailsMobile = $("#jobDetailsMobile")
    jobDetailsMobileButton = $("#jobDetailsMobile")
    hide_button = $(".hide_button")




    // for mobile and desktop device
    function appendFetchdData(job) {
        const jobTitleMobile = $("#jobTitleMobile").html(job.title)
        const jobTitleDesc = $("#jobTitleDesc").html(job.description)
        const jobCompany = $("#jobCompany").html(job.company)
        const jobSchedule = $("#jobSchedule").html(job.schedule)
        const jobCategory = $("#jobCategory").html(job.category)
        const jobType = $("#jobType").html(job.job_type)
        const job_time_posted = $("#job_time_posted").html(job.time_posted)

        // desktop
        const jobTitleDesktop = $("#jobTitleDesktop").html(job.title)
        const jobCompanyDesktop = $("#jobCompanyDesktop").html(job.company)
        const jobScheduleDesktop = $("#jobScheduleDesktop").html(job.schedule)
        const jobCategoryDesktop = $("#jobCategoryDesktop").html(job.category)
        const jobTypeDesktop = $("#jobTypeDesktop").html(job.job_type)
        const job_time_posted_desktop = $("#job_time_posted_desktop").html(job.time_posted)

        // check the screen width, if the width is larger than 500px, it shows the desktop view
        if ($(window).width() > 1024) {
            // console.log("Screen is larger than 1024px.");
            jobDetailsDesktop.removeClass("hidden")
        }
    }

    $(".each").on("click",  function() {
        const jobId = $(this).data("id")

        console.log(jobId)

        $.ajax({
            url: `${BaseURL}/${jobId}/get-single-job/`,
            method: "GET",
            success: function(data) {
                // console.log(data);
                 if (data.job) {
                    appendFetchdData(data.job);  // Pass the job data to appendFetchdData
                 } else {
                    console.error("No job data found");
                 }
            },
            error: function(xhr, status, error) {
                console.error("Error fetching job details:", error);
            }
        })
     })

    const hideJobDetailsMobile = () => {
        console.log("Button trigger dd working already !!!")
        jobDetailsMobile.addClass('hidden')
    }

    $(document).on("click", ".wrapper", () => {
        console.log("dada")
        jobDetailsMobile.removeClass('hidden');
    })

    hide_button.on("click", hideJobDetailsMobile);

  // Select the input element(s)
  var search_input = $("input[name='search']");

  // Add an event listener to the input(s)
  search_input.on("input", function () {
    console.log("input changed to:" + $(this).val());
  });
});
