{% if not (theme.duoshuo and theme.duoshuo.shortname) and not theme.duoshuo_shortname and not theme.disqus_shortname and not theme.hypercomments_id and not theme.gentie_productKey %}
  {% if theme.livere_uid %}
    <script type="text/javascript">
      (function(d, s) {
        var j, e = d.getElementsByTagName(s)[0];
        if (typeof LivereTower === 'function') { return; }
        j = d.createElement(s);
        j.src = '';
        j.async = true;
        e.parentNode.insertBefore(j, e);
      })(document, 'script');
    </script>
  {% endif %}
{% endif %}