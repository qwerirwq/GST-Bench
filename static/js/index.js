document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".self-localization-images .self-current-view").forEach(function (dragTarget) {
    var container = dragTarget.closest(".self-localization-images");
    var dragState = null;

    if (!container) {
      return;
    }

    function moveInset(clientX, clientY) {
      var containerRect = container.getBoundingClientRect();
      var targetRect = dragTarget.getBoundingClientRect();
      var nextLeft = clientX - containerRect.left - dragState.offsetX;
      var nextTop = clientY - containerRect.top - dragState.offsetY;
      var maxLeft = containerRect.width - targetRect.width;
      var maxTop = containerRect.height - targetRect.height;

      dragTarget.style.left = Math.max(0, Math.min(nextLeft, maxLeft)) + "px";
      dragTarget.style.top = Math.max(0, Math.min(nextTop, maxTop)) + "px";
      dragTarget.style.right = "auto";
    }

    dragTarget.addEventListener("pointerdown", function (event) {
      var targetRect = dragTarget.getBoundingClientRect();
      dragState = {
        offsetX: event.clientX - targetRect.left,
        offsetY: event.clientY - targetRect.top
      };

      dragTarget.classList.add("is-dragging");
      dragTarget.setPointerCapture(event.pointerId);
      event.stopPropagation();
    });

    dragTarget.addEventListener("pointermove", function (event) {
      if (!dragState) {
        return;
      }

      moveInset(event.clientX, event.clientY);
      event.stopPropagation();
    });

    function stopDragging(event) {
      if (!dragState) {
        return;
      }

      dragState = null;
      dragTarget.classList.remove("is-dragging");
      event.stopPropagation();
    }

    dragTarget.addEventListener("pointerup", stopDragging);
    dragTarget.addEventListener("pointercancel", stopDragging);
  });

  document.querySelectorAll("[data-examples-carousel]").forEach(function (carousel) {
    var track = carousel.querySelector(".examples-track");
    var slides = Array.prototype.slice.call(carousel.querySelectorAll(".example-slide"));
    var prevButton = carousel.querySelector(".carousel-prev");
    var nextButton = carousel.querySelector(".carousel-next");
    var dots = Array.prototype.slice.call(carousel.querySelectorAll(".examples-dots button"));
    var videos = Array.prototype.slice.call(carousel.querySelectorAll("video"));
    var currentIndex = 0;
    var pointerStartX = null;

    if (!track || slides.length === 0) {
      return;
    }

    function setSlide(nextIndex) {
      currentIndex = (nextIndex + slides.length) % slides.length;
      track.style.transform = "translateX(" + (-currentIndex * 100) + "%)";

      slides.forEach(function (slide, index) {
        slide.setAttribute("aria-hidden", index === currentIndex ? "false" : "true");
      });

      dots.forEach(function (dot, index) {
        var isActive = index === currentIndex;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });

      videos.forEach(function (video) {
        if (!slides[currentIndex].contains(video)) {
          video.pause();
        }
      });
    }

    if (prevButton) {
      prevButton.addEventListener("click", function () {
        setSlide(currentIndex - 1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", function () {
        setSlide(currentIndex + 1);
      });
    }

    dots.forEach(function (dot, index) {
      dot.addEventListener("click", function () {
        setSlide(index);
      });
    });

    carousel.addEventListener("pointerdown", function (event) {
      pointerStartX = event.clientX;
    });

    carousel.addEventListener("pointerup", function (event) {
      if (pointerStartX === null) {
        return;
      }

      var deltaX = event.clientX - pointerStartX;
      pointerStartX = null;

      if (Math.abs(deltaX) < 45) {
        return;
      }

      setSlide(deltaX < 0 ? currentIndex + 1 : currentIndex - 1);
    });

    carousel.addEventListener("pointercancel", function () {
      pointerStartX = null;
    });

    setSlide(0);
  });

  var leaderboardDataElement = document.getElementById("leaderboard-data");
  var leaderboardSelect = document.getElementById("leaderboard-view");
  var leaderboardTable = document.getElementById("leaderboard-table");
  var leaderboardDetails = document.getElementById("leaderboard-all-details");
  var leaderboardStatus = document.getElementById("leaderboard-status");

  if (leaderboardDataElement && leaderboardSelect && leaderboardTable && leaderboardDetails && leaderboardStatus) {
    var rankClasses = ["rank-red", "rank-orange", "rank-yellow"];

    function getScore(model, key) {
      var score = model.scores[key];
      return typeof score === "number" && Number.isFinite(score) ? score : -Infinity;
    }

    function sortModels(models, key) {
      return models.slice().sort(function (first, second) {
        var scoreDifference = getScore(second, key) - getScore(first, key);
        return scoreDifference || first.name.localeCompare(second.name);
      });
    }

    function appendCell(row, tagName, text, classNames) {
      var cell = document.createElement(tagName);
      cell.textContent = text;

      (classNames || []).forEach(function (className) {
        cell.classList.add(className);
      });

      row.appendChild(cell);
      return cell;
    }

    function interpolateColor(start, end, progress) {
      return start.map(function (channel, index) {
        return Math.round(channel + (end[index] - channel) * progress);
      });
    }

    function scoreColor(score) {
      var normalizedScore = Math.max(0, Math.min(score, 100)) / 100;
      var lowColor = [232, 82, 82];
      var middleColor = [72, 118, 232];
      var highColor = [54, 179, 126];
      var color;

      if (normalizedScore <= 0.75) {
        color = interpolateColor(lowColor, middleColor, normalizedScore / 0.75);
      } else {
        color = interpolateColor(middleColor, highColor, (normalizedScore - 0.75) / 0.25);
      }

      return "rgb(" + color.join(", ") + ")";
    }

    function appendVisualScoreCell(row, score) {
      var boundedScore = Math.max(0, Math.min(score, 100));
      var cell = document.createElement("td");
      var visual = document.createElement("div");
      var value = document.createElement("span");
      var track = document.createElement("span");
      var bar = document.createElement("span");

      cell.className = "leaderboard-visual-score";
      visual.className = "score-visual";
      value.className = "score-visual-value";
      value.textContent = score.toFixed(2);
      track.className = "score-visual-track";
      track.setAttribute("aria-hidden", "true");
      bar.className = "score-visual-bar";
      bar.style.width = boundedScore + "%";
      bar.style.backgroundColor = scoreColor(boundedScore);

      track.appendChild(bar);
      visual.appendChild(value);
      visual.appendChild(track);
      cell.appendChild(visual);
      row.appendChild(cell);
    }

    function appendScoreHeader(row, label, metric) {
      var heading = appendCell(row, "th", label, []);
      heading.setAttribute("scope", "col");

      if (metric) {
        var metricLabel = document.createElement("span");
        metricLabel.className = "leaderboard-metric";
        metricLabel.textContent = metric;
        heading.appendChild(metricLabel);
      }

      return heading;
    }

    function appendTypeCell(row, type) {
      var cell = document.createElement("td");
      var label = document.createElement("span");
      var typeClass = type.toLowerCase().replace(/[^a-z0-9]+/g, "-");

      label.className = "leaderboard-type-label is-" + typeClass;
      label.textContent = type;
      cell.appendChild(label);
      row.appendChild(cell);
    }

    function rankLabel(index) {
      var medals = ["🥇", "🥈", "🥉"];
      return index < medals.length ? medals[index] + " " + (index + 1) : String(index + 1);
    }

    function createTopRankMap(models, scoreKey) {
      var ranking = {};

      sortModels(models, scoreKey).slice(0, 3).forEach(function (model, index) {
        ranking[model.name] = index;
      });

      return ranking;
    }

    function renderLeaderboard(data, view) {
      var tableHead = leaderboardTable.querySelector("thead");
      var tableBody = leaderboardTable.querySelector("tbody");
      var task = data.tasks.find(function (item) {
        return item.key === view;
      });
      var scoreKey = task ? task.key : "avg";
      var models = view === "all" ? sortModels(data.models, "avg") : sortModels(data.models, scoreKey);
      var taskRanks = {};
      var headerRow = document.createElement("tr");
      var subtaskHeaderRow = null;

      tableHead.replaceChildren();
      tableBody.replaceChildren();
      leaderboardTable.classList.toggle("is-all-tasks", view === "all");
      leaderboardDetails.hidden = view !== "all";

      data.tasks.forEach(function (item) {
        taskRanks[item.key] = createTopRankMap(data.models, item.key);
      });

      if (view === "all") {
        var rankHeader = appendScoreHeader(headerRow, "Rank", "");
        var modelHeader = appendScoreHeader(headerRow, "Model", "");
        var taskGroups = [];

        rankHeader.rowSpan = 2;
        modelHeader.rowSpan = 2;

        data.tasks.forEach(function (item) {
          var latestGroup = taskGroups[taskGroups.length - 1];

          if (!latestGroup || latestGroup.name !== item.group) {
            taskGroups.push({name: item.group, count: 1});
          } else {
            latestGroup.count += 1;
          }
        });

        taskGroups.forEach(function (group) {
          var groupHeader = appendCell(headerRow, "th", group.name, ["leaderboard-group-heading"]);
          groupHeader.setAttribute("scope", "colgroup");
          groupHeader.colSpan = group.count;
        });

        var averageHeader = appendScoreHeader(headerRow, "Avg.", "%");
        var typeHeader = appendScoreHeader(headerRow, "Type", "");
        averageHeader.rowSpan = 2;
        typeHeader.rowSpan = 2;

        subtaskHeaderRow = document.createElement("tr");
        data.tasks.forEach(function (item) {
          appendScoreHeader(subtaskHeaderRow, item.abbreviation, item.metric + " (%)");
        });

        tableHead.appendChild(headerRow);
        tableHead.appendChild(subtaskHeaderRow);
      } else if (task) {
        appendScoreHeader(headerRow, "Rank", "");
        appendScoreHeader(headerRow, "Model", "");
        appendScoreHeader(headerRow, "Score", task.metric + " (%)");
        appendScoreHeader(headerRow, "Type", "");
        tableHead.appendChild(headerRow);
      } else {
        appendScoreHeader(headerRow, "Rank", "");
        appendScoreHeader(headerRow, "Model", "");
        appendScoreHeader(headerRow, "Avg.", "%");
        appendScoreHeader(headerRow, "Type", "");
        tableHead.appendChild(headerRow);
      }

      models.forEach(function (model, index) {
        var row = document.createElement("tr");
        appendCell(row, "td", rankLabel(index), ["leaderboard-rank"]);
        appendCell(row, "td", model.name, ["leaderboard-model"]);

        if (view === "all") {
          data.tasks.forEach(function (item) {
            var rank = taskRanks[item.key][model.name];
            var classes = ["leaderboard-score"];

            if (typeof rank === "number") {
              classes.push(rankClasses[rank]);
            }

            appendCell(row, "td", getScore(model, item.key).toFixed(2), classes);
          });
          appendCell(row, "td", getScore(model, "avg").toFixed(2), ["leaderboard-score"]);
        } else {
          appendVisualScoreCell(row, getScore(model, scoreKey));
        }

        appendTypeCell(row, model.type);
        tableBody.appendChild(row);
      });

      leaderboardStatus.hidden = true;
    }

    try {
      var data = window.GST_BENCH_LEADERBOARD;

      if (!data || !Array.isArray(data.tasks) || !Array.isArray(data.models)) {
        throw new Error("Leaderboard data is missing the tasks or models list.");
      }

      data.tasks.forEach(function (task) {
        var option = document.createElement("option");
        option.value = task.key;
        option.textContent = task.label;
        leaderboardSelect.appendChild(option);
      });

      leaderboardSelect.addEventListener("change", function () {
        renderLeaderboard(data, leaderboardSelect.value);
      });

      renderLeaderboard(data, leaderboardSelect.value);
    } catch (error) {
      leaderboardStatus.hidden = false;
      leaderboardStatus.classList.add("is-error");
      leaderboardStatus.textContent = "Unable to load leaderboard data. " + error.message;
    }
  }
});
