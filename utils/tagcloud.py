#!/usr/bin/env python

import re
import json
import fileinput
import dateutil.parser

MAX_WORDS = 200

word_counts = {}
stop_words = set(["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your"])

for line in fileinput.input():
    tweet = json.loads(line)
    for word in tweet['text'].split(' '):
        word = word.lower()
        word = word.replace(".", "")
        if len(word) == 0 or len(word) == 1: continue
        if word in stop_words: continue
        if word[0] in ["@", "#"]: continue
        if word.startswith("http://"): continue
        if word.startswith("rt"): continue
        if not re.match('^[a-z]', word): continue
        word_counts[word] = word_counts.get(word, 0) + 1

sorted_words = word_counts.keys()
sorted_words.sort(lambda a, b: cmp(word_counts[b], word_counts[a]))
top_words = sorted_words[0:MAX_WORDS]

words = []
count_range = word_counts[top_words[0]] - word_counts[top_words[-1]]
size_ratio = 200.0 / count_range
for word in top_words:
    words.append({
        "text": word, 
        "size": int(word_counts[word] * size_ratio)
    })

print """<!DOCTYPE html>
<meta charset="utf-8">
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="https://raw.github.com/jasondavies/d3-cloud/master/d3.layout.cloud.js"></script>
<body>
<script>
  var fill = d3.scale.category20();
  var words = %s

  d3.layout.cloud().size([800, 800])
      .words(words)
      .rotate(function() { return ~~(Math.random() * 2) * 90; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();

  function draw(words) {
    d3.select("body").append("svg")
        .attr("width", 1000)
        .attr("height", 1000)
      .append("g")
        .attr("transform", "translate(400,400)")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
  }
</script>
</body>
</html>
""" % json.dumps(words)
